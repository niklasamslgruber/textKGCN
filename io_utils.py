# Includes:
# - all paths
# - helper methods to read and write to / from txt, json, csv
from os.path import dirname, abspath, join


# Base Paths
def get_root_path():
    return dirname(abspath(__file__))


def get_data_path():
    return join(get_root_path(), '_data')


def get_corpus_path():
    return join(get_data_path(), 'corpus')


def get_cache_path():
    return join(get_root_path(), '_cache')


def get_plots_path():
    return join(get_root_path(), '_plots')


def get_logs_path():
    return join(get_root_path(), '_logs')


# Specific directory paths
def get_kg_data_path():
    return join(get_data_path(), 'knowledge_graphs/Wikidata')


def get_kg_relations_path():
    return join(get_kg_data_path(), 'relations')


def get_kg_triples_path():
    return join(get_kg_data_path(), 'triples')


def get_kg_data_path():
    return join(get_kg_data_path(), 'data')


def get_embeddings_cache_path():
    return join(get_root_path(), '_plots/gcn/embeddings')


# Specific file paths

# Triples
def get_all_word_triples_path(dataset):
    return join(get_kg_triples_path(), f'{dataset}_triples.csv')


def get_filtered_word_triples_path(dataset):
    return join(get_kg_triples_path(), f'{dataset}_filtered_triples.csv')


def get_document_triples_path(dataset):
    return join(get_kg_triples_path(), f'{dataset}_document_triples.csv')


# Mappings
def get_entity2id_path(dataset):
    return join(get_kg_data_path(), f'{dataset}_entity2id.csv')


def get_vocab_entities_path(dataset):
    return join(get_kg_data_path(), f'{dataset}_vocab_entities.json')


def get_vocab_relations_path(dataset):
    return join(get_kg_data_path(), f'{dataset}_vocab_relations.json')


# WikiData Data
def get_all_wiki_relations_path():
    return join(get_kg_relations_path(), 'all_wiki_relations.csv')


def get_filtered_wiki_relations_path():
    return join(get_kg_relations_path(), 'filtered_wiki_relations.csv')


def get_filtered_wiki_detailed_relations_path():
    return join(get_kg_relations_path(), 'filtered_wiki_relations_detail.csv')


# Dataset files
def get_labels_path(dataset):
    return join(get_corpus_path(), f'{dataset}_labels.txt')


def get_sentences_path(dataset):
    return join(get_corpus_path(), f'{dataset}_sentences.txt')


def get_clean_sentences_path(dataset):
    return join(get_corpus_path(), f'{dataset}_sentences_clean.txt')


def get_vocab_path(dataset):
    return join(get_corpus_path(), f'{dataset}_vocab.txt')


# Plots
def get_words_layer_path(dataset, layer):
    return join(get_plots_path(), f'{dataset}_words_layer_{layer}.png')


def get_documents_layer_path(dataset, layer):
    return join(get_plots_path(), f'{dataset}_docs_layer_{layer}.png')


# Embeddings
def get_word_embeddings_path(dataset, layer):
    return join(get_embeddings_cache_path(), f'{dataset}_word_embeddings_layer{layer}.csv')


def get_document_embeddings_path(dataset, layer):
    return join(get_embeddings_cache_path(), f'{dataset}_doc_embeddings_layer{layer}.csv')