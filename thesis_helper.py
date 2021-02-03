from os.path import exists
import seaborn as sns

from analyze_results import get_number_of_edges
from helper import file_utils as file, io_utils as io
import pandas as pd
import numpy as np
from visualization.visualize_gcn import generate_doc_labels
from visualization.visualize_tsne import reduce_dimensions, visualize_highlight

sns.set(style='darkgrid', color_codes=True)


def analyze_relations(dataset, id1, id2):
    doc2id = file.get_doc2id(dataset)
    vocab = file.get_entity2id(dataset)
    docs = file.get_sentences(dataset)
    triples = file.get_document_triples(dataset)
    filtered = file.get_filtered_triples(dataset)
    all_props = file.get_all_relations()

    connections = triples[(triples["doc1"] == id1) & (triples["doc2"] == id2)]
    details = connections["detail"].tolist()[0].split("+")
    assert len(details) == connections["relations"].tolist()[0]

    doc1 = docs[id1]
    doc2 = docs[id2]

    doc1_ids = doc2id[doc2id["doc"] == id1]["wikiID"].tolist()
    doc2_ids = doc2id[doc2id["doc"] == id2]["wikiID"].tolist()

    all_relations = doc1_ids + doc2_ids
    all_relations = list(dict.fromkeys(all_relations))

    entities_doc1 = []
    entities_doc2 = []
    result1 = filtered[(filtered["entity1"].isin(doc1_ids)) & (filtered["entity2"].isin(doc2_ids))]
    result2 = filtered[(filtered["entity2"].isin(doc1_ids)) & (filtered["entity1"].isin(doc2_ids))]
    merged_results = pd.concat([result1, result2]).reset_index(drop=True)
    assert merged_results.shape[0] == connections["relations"].tolist()[0]

    for relation in doc1_ids:
        word = vocab[vocab["wikiID"] == relation]["word"].tolist()
        entities_doc1.append([word, relation])

    for relation in doc2_ids:
        word = vocab[vocab["wikiID"] == relation]["word"].tolist()
        entities_doc2.append([word, relation])

    count1 = 0
    count2 = 0

    for w in entities_doc1:
        word = w[0][0]
        if word in doc1 and len(word) > 1:
            count1 += 1
            doc1 = doc1.replace(word, "\hl{" + word + "}")

    for w in entities_doc2:
        word = w[0][0]
        if word in doc2 and len(word) > 1:
            count2 += 1
            doc2 = doc2.replace(word, "\hl{" + word + "}")

    print(doc1)
    print("\n\n\n")
    print(doc2)

    print(entities_doc1)
    print(merged_results)

    labeld_aray = []
    for index, row in merged_results.iterrows():
        entity1 = row["entity1"]
        entity2 = row["entity2"]
        rel = row["relations"]

        word1 = vocab[vocab["wikiID"] == entity1]["word"].tolist()[0]
        word2 = vocab[vocab["wikiID"] == entity2]["word"].tolist()[0]
        desc = all_props[all_props["ID"] == rel]["label"].tolist()[0]
        labeld_aray.append([word1, desc, word2])

    labeled_df = pd.DataFrame(labeld_aray)
    print(labeled_df)


def get_max_min_values(dataset, type, n=5):
    results_log = file.get_eval_logs(dataset=dataset)
    results_log = results_log[results_log["raw_count"] == type]
    maximum = results_log.nlargest(n, columns="accuracy")
    minimum = results_log.nsmallest(n, columns="accuracy")
    return maximum, minimum


def get_base_lowest(dataset, n=5):
    results_log = file.get_eval_logs(dataset=dataset)
    minimum = results_log[results_log["wiki_enabled"] == False].nsmallest(n, columns="accuracy")
    maximum = pd.DataFrame()
    return maximum, minimum


def remove_wrongs(edges):
    for dataset in edges.keys():
        counts = edges[dataset]
        max_nonzero = len(counts) - 2
        results_log = file.get_eval_logs(dataset=dataset)
        indices = results_log[results_log["threshold"] > max_nonzero].index
        results_log.loc[indices, 'wiki_enabled'] = False
        file.save_eval_logs(results_log, dataset=dataset)


def get_graph_details(dataset):
    base_edges = file.get_base_edges(dataset)
    types = set(base_edges["edge_type"].tolist())

    for t in types:
        count = base_edges[base_edges["edge_type"] == t].shape[0]
        print(t, count)

    # print(base_edges.head())

ohsumed_colors = [
    [0.87696976, 0.53662197, 0.20161359],
     [0.39785174, 0.14077558, 0.03484343],
     [0.40281644, 0.87598413, 0.23823897],
     [0.94033192, 0.17783354, 0.65802753],
     [0.57713418, 0.1947504,  0.12719329],
     [0.44039277, 0.29924405, 0.72650093],
     [0.38028269, 0.89793327, 0.58556525],
     [0.16676958, 0.61377713, 0.73910106],
     [0.8451732,  0.646984,   0.39463175],
     [0.03802899, 0.74157645, 0.23329789],
     [0.70155728, 0.37348221, 0.67676925],
     [0.84022014, 0.39748405, 0.64789638],
     [0.83657054, 0.96644718, 0.74838346],
     [0.45796036, 0.25250949, 0.40888393],
     [0.27205942, 0.16957816, 0.51482936],
     [0.35751255, 0.36778616, 0.2032978 ],
     [0.87786575, 0.06082114, 0.73051948],
     [0.26296849, 0.92915212, 0.49388716],
     [0.05749447, 0.6363974,  0.60248133],
     [0.11981351, 0.58317452, 0.70530186],
     [0.89247519, 0.74573484, 0.61559013],
     [0.99396792, 0.15785788, 0.154068],
     [0.8410705,  0.71555522, 0.04468367]
]

mr_colors = ["red", "blue"]

r52_colors = colors = np.random.rand(52, 3)

r8_colors = ["r", "b", "g", "y", "c", "m", "k", "burlywood"]

dataset_colors = {
        "mr": mr_colors,
        "r8": r8_colors,
        "ohsumed": ohsumed_colors,
        "r52": r52_colors
        }


def analyze_doc_embeddings(dataset, path, id1, id2, filename):

    embeddings = io.read_csv(path, sep=",")
    reduced_emb_doc = reduce_dimensions(embeddings)

    doc_labels = generate_doc_labels(embeddings, dataset)
    label1 = doc_labels[id1]
    label2 = doc_labels[id2]
    # assert label1 == label2
    visualize_highlight(reduced_emb_doc, id1, id2, label1, filename=filename, labels=doc_labels, colors=dataset_colors[dataset])


top_words_dict = {
    "ohsumed": {},
    "r8": {},
    "r52": {},
    "mr": {}
    }


def analyze_word_embeddings(dataset, path, threshold, edge_type, best, n=10):
    global top_words_dict
    embeddings = io.read_csv(path, sep=",")
    embeddings_array = embeddings.to_numpy().tolist()
    unique_labels = sorted(list(set([label.split("\t")[2] for label in file.get_labels(dataset)])), reverse=True)
    vocab = file.get_vocab(dataset)
    max_indices = []
    max_values = []
    all_words = []
    all_labels = []
    results_dict = {}
    for index, emb in enumerate(embeddings_array):
        array = np.array(emb)
        max_index = array.argmax()
        max_indices.append(max_index)
        max_values.append(array[max_index])
        all_words.append(vocab[index])
        all_labels.append(unique_labels[max_index])
        results_dict[index] = {
            "max_index": max_index,
            "max_value": array[max_index],
            "word": vocab[index],
            "label": unique_labels[max_index]
            }

    assert len(max_values) == len(max_indices) == len(all_words) == len(all_labels)
    results_df = pd.DataFrame.from_dict(results_dict,orient="index")

    top_words = {}
    for u_label in unique_labels:
        largest = results_df[results_df["label"] == u_label].nlargest(n, columns="max_value")["word"].tolist()
        top_words[u_label] = largest

    # print(top_words)
    # key = f"{threshold}:{edge_type}"
    if best:
        top_words_dict[dataset][edge_type] = top_words


def get_embeddings_from_disk(maximum, minimum, type, dataset, layer):
    max_counter = 0
    min_counter = 0
    for index, row in maximum.iterrows():
            directory = row["time"]
            doc_path = f"/Volumes/Data/NewLogs/{dataset.title()}/{directory}/plots/gcn_embeddings/{dataset}_doc_embeddings_layer{layer}.csv"
            word_path = f"/Volumes/Data/NewLogs/{dataset.title()}/{directory}/plots/gcn_embeddings/{dataset}_word_embeddings_layer{layer}.csv"

            if exists(doc_path):
                analyze_doc_embeddings(dataset, doc_path, 158, 175, f"{io.get_basic_embeddings_plots_path(dataset)}/{dataset}_{type}_max_doc_emb_layer{layer}.png")
                # analyze_word_embeddings(dataset, word_path, row["threshold"], type, True, n=5)
                print(f"Plotted {directory} for {dataset}")
                break
            else:
                max_counter += 1

    if max_counter == maximum.shape[0]:
        print("No files found for maximum")

    for index, row in minimum.iterrows():
            directory = row["time"]
            doc_path = f"/Volumes/Data/NewLogs/{dataset.title()}/{directory}/plots/gcn_embeddings/{dataset}_doc_embeddings_layer{layer}.csv"
            word_path = f"/Volumes/Data/NewLogs/{dataset.title()}/{directory}/plots/gcn_embeddings/{dataset}_word_embeddings_layer{layer}.csv"

            if exists(doc_path):
                analyze_doc_embeddings(dataset, doc_path, 158, 175, f"{io.get_basic_embeddings_plots_path(dataset)}/{dataset}_{type}_min_doc_emb_layer{layer}.png")
                # analyze_word_embeddings(dataset, word_path, row["threshold"], type, type == "base", n=5)
                print(f"Plotted {directory} for {dataset}")
                break
            else:
                min_counter += 1

    if min_counter == minimum.shape[0]:
        print("No files found for minimum")

def plot_all():
    datasets = ["mr", "r8", "r52", "ohsumed"]
    # types = ["count", "count_norm", "count_norm_pmi", "idf", "idf_norm", "idf_norm_pmi", "idf_wiki", "idf_wiki_norm",
    #          "idf_wiki_norm_pmi"]
    types = ["count", "idf_wiki", "idf_wiki_norm", "idf_wiki_norm_pmi"]

    for dataset in ["r52"]:
        for t in types:
            maximum, minimum = get_max_min_values(dataset, t, 10)
            if t == "count":
                minimum = pd.DataFrame()
            elif "idf_wiki" in t:
                maximum = pd.DataFrame()
            get_embeddings_from_disk(maximum, minimum, t, dataset, layer=1)
            get_embeddings_from_disk(maximum, minimum, t, dataset, layer=0)


        maximum, minimum = get_base_lowest(dataset, 10)
        get_embeddings_from_disk(maximum, minimum, "base", dataset, layer=1)
        get_embeddings_from_disk(maximum, minimum, "base", dataset, layer=0)



if __name__ == '__main__':
    edges = get_number_of_edges()
    remove_wrongs(edges)