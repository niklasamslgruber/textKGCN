import json
from os.path import dirname, abspath, join, isfile
from helper import utils
from config import FLAGS
import pandas as pd


# Base Paths
def get_root_path():
    return dirname(dirname(abspath(__file__)))


def get_data_path():
    return path(join(get_root_path(), '_data'))


def get_corpus_path():
    return path(join(get_data_path(), 'corpus'))


def get_cache_path():
    return path(join(get_root_path(), '_cache'))


def get_plots_path():
    return path(join(get_root_path(), '_plots'))


def get_logs_path():
    return path(join(get_root_path(), '_logs'))


# Specific directory paths
def get_kg_base_path():
    return path(join(get_data_path(), 'wikidata'))


def get_kg_relations_path():
    return path(join(get_kg_base_path(), 'relations'))


def get_kg_triples_path():
    return path(join(get_kg_base_path(), 'triples'))


def get_kg_data_path():
    return path(join(get_kg_base_path(), 'data'))


def get_embeddings_cache_path():
    return path(join(get_cache_path(), 'gcn_embeddings'))

# Specific file paths


# Triples
def get_all_word_triples_path(dataset=FLAGS.dataset):
    return join(get_kg_triples_path(), f'{dataset}_triples.csv')


def get_filtered_word_triples_path(dataset=FLAGS.dataset):
    return join(get_kg_triples_path(), f'{dataset}_filtered_triples.csv')


def get_document_triples_path(dataset=FLAGS.dataset):
    return join(get_kg_triples_path(), f'{dataset}_document_triples.csv')


def get_document_triples_pickle_path(dataset=FLAGS.dataset):
    return join(get_kg_triples_path(), f'{dataset}_document_triples.pickle')


# Mappings
def get_entity2id_path(dataset=FLAGS.dataset):
    return join(get_kg_data_path(), f'{dataset}_entity2id.csv')


def get_doc2id_path(dataset=FLAGS.dataset):
    return join(get_kg_data_path(), f'{dataset}_doc2id.csv')


def get_vocab_entities_path(dataset=FLAGS.dataset):
    return join(get_kg_data_path(), f'{dataset}_vocab_entities.json')


def get_vocab_relations_path(dataset=FLAGS.dataset):
    return join(get_kg_data_path(), f'{dataset}_vocab_relations.json')


# WikiData Data
def get_all_wiki_relations_path():
    return join(get_kg_relations_path(), 'all_wiki_relations.csv')


def get_filtered_wiki_relations_path():
    return join(get_kg_relations_path(), 'filtered_wiki_relations.csv')


# Dataset files
def get_labels_path(dataset=FLAGS.dataset):
    return join(get_corpus_path(), f'{dataset}_labels.txt')


def get_sentences_path(dataset=FLAGS.dataset):
    return join(get_corpus_path(), f'{dataset}_sentences.txt')


def get_clean_sentences_path(dataset=FLAGS.dataset):
    return join(get_corpus_path(), f'{dataset}_sentences_clean.txt')


def get_vocab_path(dataset=FLAGS.dataset):
    return join(get_corpus_path(), f'{dataset}_vocab.txt')


def get_nouns_vocab(dataset=FLAGS.dataset):
    return join(get_kg_data_path(), f'{dataset}_vocab_nouns.txt')


def get_nouns_path(dataset=FLAGS.dataset):
    return join(get_kg_data_path(), f'{dataset}_nouns.txt')


def get_normalized_nouns_path(dataset=FLAGS.dataset):
    return join(get_kg_data_path(), f'{dataset}_nouns_normalized.txt')


# Plots
def get_words_layer_plot_path(layer, dataset=FLAGS.dataset):
    word_path = path(join(get_plots_path(), 'embeddings/words'))
    return join(word_path, f'{dataset}_words_layer_{layer}.png')


def get_documents_layer_plot_path(layer, dataset=FLAGS.dataset):
    doc_path = path(join(get_plots_path(), 'embeddings/docs'))
    return join(doc_path, f'{dataset}_docs_layer_{layer}.png')


def get_results_plot_path(metric, dataset=FLAGS.dataset):
    results_path = path(join(get_plots_path(), f'results/{metric}'))
    return join(results_path, f'{dataset}_eval_results_{metric}.png')


def get_eval_loss_plot_path(dataset=FLAGS.dataset):
    results_path = path(join(get_plots_path(), f'results/val_loss'))
    return join(results_path, f'{dataset}_val_loss.png')


# Embeddings
def get_word_embeddings_path(layer, dataset=FLAGS.dataset):
    return join(get_embeddings_cache_path(), f'{dataset}_word_embeddings_layer{layer}.csv')


def get_document_embeddings_path(layer, dataset=FLAGS.dataset):
    return join(get_embeddings_cache_path(), f'{dataset}_doc_embeddings_layer{layer}.csv')


# Evaluation logs
def get_eval_log_path(dataset=FLAGS.dataset):
    return join(path(join(get_data_path(), 'results_log')), f'{dataset}_eval_log.csv')


# JSON
def read_json(path):
    assert path.endswith('.json')

    json_dict = {}
    if isfile(path):
        with open(path, 'r') as output:
            json_dict = json.load(output)
        output.close()
    return json_dict


def write_json(path, data):
    assert path.endswith('.json')

    with open(path, "w") as output:
        json.dump(data, output, indent=4)
    output.close()


# TXT
def write_txt(data, path, sep="\n"):
    assert path.endswith('.txt')
    data_to_write = map(lambda item: item.replace("\n", ""), data)
    f = open(path, 'w')
    f.writelines(sep.join(data_to_write))
    f.close()


def read_txt(path):
    assert path.endswith('.txt')
    data = []
    if isfile(path):
        file = open(path, 'r')
        for line in file.readlines():
            data.append(line.strip())
        file.close()
    else:
        raise ValueError(f'File not found: {path}')
    return data


# CSV
def write_csv(path, array, sep, header=True):
    assert path.endswith('.csv')
    data = pd.DataFrame(array)
    data.to_csv(path, index=False, header=header, sep=sep)


def read_csv(path, sep):
    assert path.endswith('.csv')
    return pd.read_csv(path, index_col=None, sep=sep)


# Helper
def path(path):
    utils.create_dir_if_not_exists(path)
    return path

