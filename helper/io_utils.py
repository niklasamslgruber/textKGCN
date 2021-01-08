import json
from os.path import dirname, abspath, join, isfile
from helper import utils
from config import FLAGS
import pytz
import datetime
import pandas as pd


# Base Paths
def get_root_path():
    return dirname(dirname(abspath(__file__)))


def get_data_path():
    return path(join(get_root_path(), '_data'))


def get_dataset_path(dataset=FLAGS.dataset):
    return path(join(get_data_path(), dataset))


def get_corpus_path(dataset=FLAGS.dataset):
    return path(join(get_dataset_path(dataset), 'corpus'))


def get_cache_path():
    return path(join(get_root_path(), '_cache'))


def get_plots_path(dataset=FLAGS.dataset):
    return path(join(get_logs_path(dataset), 'plots'))


def get_logs_path(dataset=FLAGS.dataset):
    return path(join(get_dataset_path(dataset), '_logs', get_ts()))


def get_basic_plots_path(dataset=FLAGS.dataset):
    return path(join(get_root_path(), f'plots/{dataset}'))


def get_latex_path(dataset=FLAGS.dataset):
    return path(join(get_root_path(), f'latex/{dataset}'))


def get_ordered_path(dataset=FLAGS.dataset):
    return path(join(get_root_path(), f'ordered/{dataset}'))


# Specific directory paths
def get_kg_base_path(dataset=FLAGS.dataset):
    return path(join(get_dataset_path(dataset), 'triples'))


def get_kg_relations_path():
    return path(join(get_data_path(), 'relations'))


def get_kg_triples_path(dataset=FLAGS.dataset):
    return path(join(get_dataset_path(dataset), 'triples'))


def get_kg_data_path(dataset=FLAGS.dataset):
    return path(join(get_dataset_path(dataset), 'data'))


def get_embeddings_cache_path(dataset=FLAGS.dataset):
    return path(join(get_plots_path(dataset), 'gcn_embeddings'))


# Specific file paths


# Triples
def get_all_word_triples_path(dataset=FLAGS.dataset):
    return join(get_kg_triples_path(dataset), f'{dataset}_triples.csv')


def get_filtered_word_triples_path(dataset=FLAGS.dataset):
    return join(get_kg_triples_path(dataset), f'{dataset}_filtered_triples_{FLAGS.version}.csv')


def get_document_triples_path(dataset=FLAGS.dataset):
    return join(get_kg_triples_path(dataset), f'{dataset}_document_triples_{FLAGS.version}.pickle.bz2')


def get_document_triples_metrics_path(dataset=FLAGS.dataset):
    return join(get_kg_triples_path(dataset), f'{dataset}_document_triples_metrics_{FLAGS.version}.pickle.bz2')


def get_ordered_document_triples_metrics_path(edge_type, dataset=FLAGS.dataset):
    return join(get_ordered_path(dataset), f'{dataset}_ordered_document_triples_{edge_type}_{FLAGS.version}.csv')


# Mappings
def get_entity2id_path(dataset=FLAGS.dataset):
    return join(get_kg_data_path(dataset), f'{dataset}_entity2id.csv')


def get_doc2id_path(dataset=FLAGS.dataset):
    return join(get_kg_data_path(dataset), f'{dataset}_doc2id.csv')


def get_doc2relations_path(dataset=FLAGS.dataset):
    return join(get_kg_data_path(dataset), f'{dataset}_doc2relations_{FLAGS.version}.txt')


def get_doc2idf_path(dataset=FLAGS.dataset):
    return join(get_kg_data_path(dataset), f'{dataset}_doc2idf_{FLAGS.version}.csv')


def get_base_edges_path(dataset=FLAGS.dataset):
    return join(get_kg_data_path(dataset), f'{dataset}_base_edges_{FLAGS.version}.pickle.bz2')


def get_original_edges_path(dataset=FLAGS.dataset):
    return join(get_kg_data_path(dataset), f'{dataset}_original_edges.pickle.bz2')


def get_vocab_entities_path(dataset=FLAGS.dataset):
    return join(get_kg_data_path(dataset), f'{dataset}_vocab_entities.json')


def get_vocab_relations_path(dataset=FLAGS.dataset):
    return join(get_kg_data_path(dataset), f'{dataset}_vocab_relations.json')


# WikiData Data
def get_all_wiki_relations_path():
    return join(get_kg_relations_path(), 'all_wiki_relations.csv')


def get_filtered_wiki_relations_path():
    return join(get_kg_relations_path(), f'filtered_wiki_relations_{FLAGS.version}.csv')


# Dataset files
def get_labels_path(dataset=FLAGS.dataset):
    return join(get_corpus_path(dataset), f'{dataset}_labels.txt')


def get_sentences_path(dataset=FLAGS.dataset):
    return join(get_corpus_path(dataset), f'{dataset}_sentences.txt')


def get_clean_sentences_path(dataset=FLAGS.dataset):
    return join(get_corpus_path(dataset), f'{dataset}_sentences_clean.txt')


def get_vocab_path(dataset=FLAGS.dataset):
    return join(get_corpus_path(dataset), f'{dataset}_vocab.txt')


def get_nouns_vocab(dataset=FLAGS.dataset):
    return join(get_kg_data_path(dataset), f'{dataset}_vocab_nouns.txt')


def get_nouns_path(dataset=FLAGS.dataset):
    return join(get_kg_data_path(dataset), f'{dataset}_nouns.txt')


def get_normalized_nouns_path(dataset=FLAGS.dataset):
    return join(get_kg_data_path(dataset), f'{dataset}_nouns_normalized.txt')


# Plots
def get_words_layer_plot_path(layer, dataset=FLAGS.dataset):
    word_path = path(join(get_plots_path(dataset), 'words'))
    return join(word_path, f'{dataset}_words_layer_{layer}.png')


def get_documents_layer_plot_path(layer, dataset=FLAGS.dataset):
    doc_path = path(join(get_plots_path(dataset), 'docs'))
    return join(doc_path, f'{dataset}_docs_layer_{layer}.png')


def get_results_plot_path(metric, dataset=FLAGS.dataset):
    results_path = path(join(get_plots_path(dataset), f'results/{metric}'))
    return join(results_path, f'{dataset}_eval_results_{metric}.png')


def get_eval_loss_plot_path(dataset=FLAGS.dataset):
    results_path = path(join(get_plots_path(dataset), f'results/val_loss'))
    return join(results_path, f'{dataset}_val_loss.png')


# Embeddings
def get_word_embeddings_path(layer, dataset=FLAGS.dataset):
    return join(get_embeddings_cache_path(dataset), f'{dataset}_word_embeddings_layer{layer}.csv')


def get_document_embeddings_path(layer, dataset=FLAGS.dataset):
    return join(get_embeddings_cache_path(dataset), f'{dataset}_doc_embeddings_layer{layer}.csv')


# Evaluation logs
def get_eval_log_path(dataset=FLAGS.dataset, version=FLAGS.version):
    return join(path(join(get_data_path(), 'results_log')), f'{dataset}_eval_{version}.csv')


def get_result_log_path(dataset=FLAGS.dataset):
    return join(get_logs_path(dataset), f'{dataset}_result.json')


def get_eval_count_path(dataset=FLAGS.dataset, version=FLAGS.version):
    return join(path(join(get_data_path(), 'results_log/counts')), f'{dataset}_eval_counts_{version}.json')


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
    return pd.read_csv(path, index_col=None, sep=sep, keep_default_na=False)


# Pickle
def write_pickle(path, data):
    assert path.endswith('.pickle.bz2')
    data.to_pickle(path, compression="bz2")


def read_pickle(path):
    assert path.endswith('.pickle.bz2')
    return pd.read_pickle(path, compression="bz2")


# Helper
def path(path):
    utils.create_dir_if_not_exists(path)
    return path


timestamp = None


def get_ts():
    global timestamp
    if not timestamp:
        timestamp = get_current_ts()
    return timestamp


def get_current_ts(zone='Europe/Berlin'):
    return datetime.datetime.now(pytz.timezone(zone)).strftime(
        '%d-%m-%Y-T%H-%M-%S.%f')
