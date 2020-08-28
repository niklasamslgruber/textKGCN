import numpy as np
import random
import torch
from torch_geometric.data import Data as PyGSingleGraphData
import scipy.sparse as sp


class TextDataset(object):
    def __init__(self, name, sparse_graph, labels, vocab, word_id_map, docs_dict, loaded_dict, tvt='all',
                 train_test_split=None):
        if loaded_dict is not None:  # restore from content loaded from disk
            self.__dict__ = loaded_dict
            return
        self.name = name
        self.graph = sparse_graph
        self.labels = labels  # Classification of each document
        if 'twitter_asian_prejudice' in name:
            if 'sentiment' not in name:
                self.labels = ['discussion_of_eastasian_prejudice' if label == 'counter_speech' else label for label in
                               self.labels]
            else:
                if 'neutral' not in labels:
                    sentiment_labels = []
                    neutral_pos_labels = ["none_of_the_above", "counter_speech", "discussion_of_eastasian_prejudice"]
                    for label in labels:
                        if label in neutral_pos_labels:
                            sentiment_labels.append("neutral")
                        else:
                            sentiment_labels.append("negative")
                    self.labels = sentiment_labels
        self.label_dict = {label: i for i, label in enumerate(list(set(self.labels)))}  # Key of the labels
        self.label_inds = np.asarray([self.label_dict[label] for label in self.labels])  # Classification of documents with label key
        self.vocab = vocab  # All unique words
        self.word_id_map = word_id_map  # ID of each word
        self.docs = docs_dict  # Documents as {key: id, value: text}
        self.node_ids = list(self.docs.keys())  # Document IDs
        print(f"Hallo: {len(self.node_ids)}")
        self.tvt = tvt
        self.train_test_split = train_test_split

    def tvt_split(self, split_points, tvt_list, seed):
        if self.train_test_split is None:
            doc_id_chunks = self._chunk_doc_ids(split_points, seed)
        else:
            train_ids = []
            test_ids = []
            for k, v in self.train_test_split.items():
                if v == 'test':
                    test_ids.append(k)
                elif v == 'train':
                    train_ids.append(k)
                else:
                    raise ValueError
            num_val = int(len(train_ids) * 0.1)
            random.Random(seed).shuffle(train_ids)
            val_ids = train_ids[:num_val]
            train_ids = train_ids[num_val:]
            doc_id_chunks = [train_ids, val_ids, test_ids]
        sub_dataset = []
        for i, chunk in enumerate(doc_id_chunks):
            docs = {doc_id: self.docs[doc_id] for doc_id in chunk}
            sub_dataset.append(TextDataset(self.name, self.graph, self.labels, self.vocab,
                                           self.word_id_map, docs, None, tvt_list[i]))
        return sub_dataset

    def _chunk_doc_ids(self, split_points, seed):
        ids = sorted(self.docs.keys())
        id_chunks = self._chunk_list(ids, split_points, seed)
        return id_chunks

    def _chunk_list(self, li, split_points, seed):
        rtn = []
        random.Random(seed).shuffle(li)
        left = 0
        split_indices = [int(len(li) * sp) for sp in split_points]
        for si in split_indices:
            right = left + si
            if type(right) is not int or right <= 0 or right >= len(li):
                raise ValueError('Wrong split_points {}'.format(split_points))
            take = li[left:right]
            rtn.append(take)
            left = right
        # The last chunk is inferred.
        rtn.append(li[left:])
        return rtn

    def init_node_feats(self, device):
        num_nodes = self.graph.shape[0]
        identity = sp.identity(num_nodes)
        ind0, ind1, values = sp.find(identity)
        inds = np.stack((ind0, ind1), axis=0)
        self.node_feats = torch.sparse_coo_tensor(inds, values, device=device, dtype=torch.float)


    def get_pyg_graph(self, device):
        if not hasattr(self, "pyg_graph"):
            adj = self.graph
            A = adj.tocoo()
            row = torch.from_numpy(A.row).to(torch.long).to(device)
            col = torch.from_numpy(A.col).to(torch.long).to(device)
            edge_index = torch.stack([row, col], dim=0)
            edge_weight = torch.from_numpy(A.data).to(torch.float).to(device)
            if type(self.node_feats) is not torch.Tensor:
                gx = torch.tensor(self.node_feats, dtype=torch.float32, device=device)
            else:
                gx = self.node_feats
            self.pyg_graph = PyGSingleGraphData(x=gx, edge_index=edge_index, edge_attr=edge_weight, y=None)
        return self.pyg_graph