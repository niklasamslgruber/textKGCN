import numpy as np
from helper import io_utils as io, file_utils as file
from config import FLAGS
from visualization.visualize_tsne import visualize, reduce_dimensions


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
    file.save_document_embeddings(embeddings, layer)

    labels = generate_doc_labels(embeddings)
    plot_embeddings(embeddings, labels, io.get_documents_layer_plot_path(layer))


def plot_words(embeddings, layer):
    file.save_word_embeddings(embeddings, layer)

    labels = generate_word_labels(embeddings)
    plot_embeddings(embeddings, labels, io.get_words_layer_plot_path(layer))


def plot_embeddings(embeddings, labels, path):
    reduced_emb = reduce_dimensions(embeddings)
    visualize(reduced_emb, filename=path, labels=labels)


def generate_doc_labels(embeddings):
    # Labels based on the "_labels.txt" file
    labels = file.get_labels()[0:len(embeddings)]
    label_index = 2 if "presplit" in FLAGS.dataset else 0
    doc_labels = list(map(lambda label: label.split(sep="\t")[label_index], labels))
    return doc_labels


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
def visualize_from_cache():
    counter = 0
    while counter < 2:
        word_emb = file.get_word_embeddings(counter)
        doc_emb = file.get_doc_embeddings(counter)

        reduced_emb_doc = reduce_dimensions(doc_emb)
        reduced_emb_word = reduce_dimensions(word_emb)
        doc_labels = generate_doc_labels(doc_emb)
        word_labels = generate_word_labels(word_emb)

        visualize(reduced_emb_word, filename=io.get_words_layer_plot_path(counter), labels=word_labels)
        visualize(reduced_emb_doc, filename=io.get_documents_layer_plot_path(counter), labels=doc_labels)
        counter += 1
