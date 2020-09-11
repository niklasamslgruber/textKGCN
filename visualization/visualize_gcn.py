from os.path import join, isfile
import pandas as pd
from config import FLAGS
from utils import get_corpus_path
from visualization.visualize_tsne import visualize, reduce_dimensions
import numpy as np


def plot(model, number_of_docs):
    current_layer = 0
    for layer in model.layers:
        embeddings = layer.acted_embeddings
        doc_embeddings = embeddings[0:number_of_docs]
        word_embeddings = embeddings[number_of_docs:]

        assert len(doc_embeddings) == number_of_docs
        assert len(word_embeddings) == (len(embeddings) - number_of_docs)

        plot_documents(doc_embeddings, current_layer)
        plot_words(word_embeddings, current_layer)
        current_layer += 1


def plot_documents(embeddings, layer):
    np.savetxt(f"_plots/gcn/embeddings/{FLAGS.dataset}_doc_embeddings_layer{layer}.csv", embeddings.numpy(),
               delimiter=",")
    labels = generate_doc_labels(embeddings)
    plot_embeddings(embeddings, labels, f"_plots/gcn/docs_layer_{layer}.png")


def plot_words(embeddings, layer):
    np.savetxt(f"_plots/gcn/embeddings/{FLAGS.dataset}_word_embeddings_layer{layer}.csv", embeddings.numpy(),
               delimiter=",")
    labels = generate_word_labels(embeddings)
    plot_embeddings(embeddings, labels, f"_plots/gcn/words_layer_{layer}.png")


def plot_embeddings(embeddings, labels, path):
    reduced_emb = reduce_dimensions(embeddings)
    visualize(reduced_emb, filename=path, labels=labels)


def generate_doc_labels(embeddings):
    # Labels based on the "_labels.txt" file
    labels_path = join(get_corpus_path(), FLAGS.dataset + '_labels.txt')
    labels = []
    if isfile(labels_path):
        file = open(labels_path, "rb")
        should_split = "ag" in FLAGS.dataset or "r8" in FLAGS.dataset
        for line in file.readlines()[0:len(embeddings)]:
            words = line.strip().decode()
            if should_split:
                words = words.split("\t")[2]
            labels.append(words)
            file.close()
    return labels


def generate_word_labels(embeddings):
    # Node gets the highest dimension as label (assumption from paper)
    max_indices = []
    for emb in embeddings:
        array = np.array(emb)
        max_index = array.argmax()
        max_indices.append(max_index)

    print(f'Number of labels: {len(set(max_indices))}')
    return max_indices


# Helper method
def read_embeddings():
    counter = 0
    while counter < 2:
        word_emb = pd.read_csv(f"_plots/gcn/embeddings/{FLAGS.dataset}_word_embeddings_layer{counter}.csv", delimiter=",", header=None).to_numpy()
        doc_emb = pd.read_csv(f"_plots/gcn/embeddings/{FLAGS.dataset}_doc_embeddings_layer{counter}.csv", delimiter=",", header=None).to_numpy()
        reduced_emb_doc = reduce_dimensions(doc_emb)
        reduced_emb_word = reduce_dimensions(word_emb)
        doc_labels = generate_doc_labels(doc_emb)
        word_labels = generate_word_labels(word_emb)
        visualize(reduced_emb_word, filename=f'_plots/gcn/{FLAGS.dataset}_words_layer_{counter}.png', labels=word_labels)
        visualize(reduced_emb_doc, filename=f'_plots/gcn/{FLAGS.dataset}_docs_layer_{counter}.png', labels=doc_labels)
        counter += 1



