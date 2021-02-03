from collections import defaultdict
from math import log
from os.path import exists
import scipy.sparse as sp
from tqdm import tqdm
from config import FLAGS
from helper import io_utils as io, file_utils as file
from loader.dataset import TextDataset
import pandas as pd


def build_text_graph_dataset(dataset, window_size):
    if "prejudice_small" in dataset:
        dataset_name = "_".join(dataset.split("_")[:-1])
    else:
        dataset_name = dataset
    labels_path = io.get_labels_path(dataset_name)
    labels = pd.read_csv(labels_path, header=None, sep='\t')
    doc_list = file.get_cleaned_sentences(dataset_name)

    assert len(labels) == len(doc_list)
    if 'small' in dataset:
        labels_list = labels.iloc[0:, 0].tolist()
        split_dict = None
    else:
        labels_list = labels.iloc[0:, 2].tolist()
        split = labels.iloc[0:, 1].tolist()
        split_dict = {}
        for i, v in enumerate(split):
            split_dict[i] = v

    word_freq = get_vocab(doc_list)
    vocab = list(word_freq.keys())
    words_in_docs, word_doc_freq = build_word_doc_edges(doc_list)
    print(f"Number of words: {len(words_in_docs)}")
    word_id_map = {word: i for i, word in enumerate(vocab)}

    sparse_graph = build_edges(doc_list, word_id_map, vocab, word_doc_freq, window_size)
    docs_dict = {i: doc for i, doc in enumerate(doc_list)}
    return TextDataset(dataset, sparse_graph, labels_list, vocab, word_id_map, docs_dict, None,
                       train_test_split=split_dict)


def build_edges(doc_list, word_id_map, vocab, word_doc_freq, window_size=20):
    # constructing all windows
    windows = []
    for doc_words in doc_list:
        words = doc_words.split()
        doc_length = len(words)
        if doc_length <= window_size:
            windows.append(words)
        else:
            for i in range(doc_length - window_size + 1):
                window = words[i: i + window_size]
                windows.append(window)
    # constructing all single word frequency
    word_window_freq = defaultdict(int)
    for window in windows:
        appeared = set()
        for word in window:
            if word not in appeared:
                word_window_freq[word] += 1
                appeared.add(word)
    # constructing word pair count frequency
    word_pair_count = defaultdict(int)
    for window in tqdm(windows):
        for i in range(1, len(window)):
            for j in range(i):
                word_i = window[i]
                word_j = window[j]
                word_i_id = word_id_map[word_i]
                word_j_id = word_id_map[word_j]
                if word_i_id == word_j_id:
                    continue
                word_pair_count[(word_i_id, word_j_id)] += 1
                word_pair_count[(word_j_id, word_i_id)] += 1
    row = []
    col = []
    weight = []
    edge_type = []

    # pmi as weights
    num_docs = len(doc_list)
    num_window = len(windows)
    for word_id_pair, count in tqdm(word_pair_count.items()):
        i, j = word_id_pair[0], word_id_pair[1]
        word_freq_i = word_window_freq[vocab[i]]
        word_freq_j = word_window_freq[vocab[j]]
        pmi = log((1.0 * count / num_window) /
                  (1.0 * word_freq_i * word_freq_j / (num_window * num_window)))
        if pmi <= 0:
            continue
        row.append(num_docs + i)
        col.append(num_docs + j)
        weight.append(pmi)
        edge_type.append("pmi")

    # frequency of document word pair
    doc_word_freq = defaultdict(int)
    for i, doc_words in enumerate(doc_list):
        words = doc_words.split()
        for word in words:
            word_id = word_id_map[word]
            doc_word_str = (i, word_id)
            doc_word_freq[doc_word_str] += 1

    print(f"Number of docs: {len(doc_list)}")
    for i, doc_words in enumerate(doc_list):
        words = doc_words.split()
        doc_word_set = set()
        for word in words:
            if word in doc_word_set:
                continue
            word_id = word_id_map[word]
            freq = doc_word_freq[(i, word_id)]
            row.append(i)
            col.append(num_docs + word_id)
            idf = log(1.0 * num_docs /
                      word_doc_freq[vocab[word_id]])
            weight.append(freq * idf)
            doc_word_set.add(word)
            edge_type.append("idf")

    base_edges = pd.DataFrame({
        "row": row,
        "col": col,
        "weight": weight,
        "edge_type": edge_type
        })
    # save_edges(base_edges)

    if FLAGS.use_wikidata:
        # Append doc2doc edges
        if FLAGS.drop_out:
            document_triples = drop_out(10)
        else:
            document_triples = file.get_document_triples_metrics()
        old_size = document_triples.shape[0]

        # Filter all relations with number of relations below threshold
        document_triples = document_triples[document_triples["count"] > FLAGS.threshold]
        print(f"doc2doc edge count threshold ({FLAGS.threshold}) filtered out: {old_size - document_triples.shape[0]}")

        weight_key = FLAGS.method
        row_doc = document_triples["doc1"].tolist()
        col_doc = document_triples["doc2"].tolist()
        weight_doc = document_triples[weight_key].tolist()
        print(f"Added {len(row_doc)} doc2doc edges with weight: {weight_key}")
        assert len(row_doc) == len(col_doc) == len(weight_doc)
        row += row_doc
        col += col_doc
        weight += weight_doc

    number_nodes = num_docs + len(vocab)
    adj_mat = sp.csr_matrix((weight, (row, col)), shape=(number_nodes, number_nodes))
    adj = adj_mat + adj_mat.T.multiply(adj_mat.T > adj_mat) - adj_mat.multiply(adj_mat.T > adj_mat)
    return adj


def save_edges(base_edges):
    # if exists(io.get_base_edges_path()):
    #     print("Edge file already exists")
    #     return
    file.save_original_edges(base_edges)

    metrics = file.get_document_triples_metrics()
    edge_types = ["count", "idf", "idf_wiki", "count_norm", "count_norm_pmi", "idf_norm", "idf_wiki_norm", "idf_norm_pmi", "idf_wiki_norm_pmi"]
    row = metrics["doc1"].tolist()
    col = metrics["doc2"].tolist()

    dataframes = []
    for t in edge_types:
        if t == "idf":
            key = "idf_doc"
        else:
            key = t
        df = pd.DataFrame({
            "row": row,
            "col": col,
            "weight": metrics[t].tolist(),
            "edge_type": [key] * len(row)
            })
        dataframes.append(df)
    assert len(dataframes) == len(edge_types)
    dataframes.append(base_edges)
    shapes = [x.shape[0] for x in dataframes]
    all_edges = pd.concat(dataframes)
    all_edges.columns = ["row", "col", "weight", "edge_type"]
    assert all_edges.shape[0] == sum(shapes)
    print(all_edges.shape)
    file.save_base_edges(all_edges)


def get_vocab(text_list):
    word_freq = defaultdict(int)
    for doc_words in text_list:
        words = doc_words.split()
        for word in words:
            word_freq[word] += 1
    return word_freq


def build_word_doc_edges(doc_list):
    # build all docs that a word is contained in
    words_in_docs = defaultdict(set)
    for i, doc_words in enumerate(doc_list):
        words = doc_words.split()
        for word in words:
            words_in_docs[word].add(i)

    word_doc_freq = {}
    for word, doc_list in words_in_docs.items():
        word_doc_freq[word] = len(doc_list)

    return words_in_docs, word_doc_freq


def drop_out(ratio=10):
    document_triples = file.get_document_triples_metrics()
    old_size = document_triples.shape[0]
    fraction = document_triples.sample(frac=1-ratio/100)

    assert int(round(old_size * (1-ratio/100), 0)) == fraction.shape[0]
    return fraction
