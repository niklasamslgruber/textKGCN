from os.path import exists
from helper import io_utils as io
from config import FLAGS


# Embeddings
def get_word_embeddings(layer):
    path = io.get_word_embeddings_path(layer)
    exist(path, "No cached embeddings. Run the model first with the --plot option enabled.")
    return io.read_csv(path, sep=",").to_numpy()


def get_doc_embeddings(layer):
    path = io.get_document_embeddings_path(layer)
    exist(path, "No cached embeddings. Run the model first with the --plot option enabled.")
    return io.read_csv(path, sep=",").to_numpy()


def save_word_embeddings(data, layer):
    io.write_csv(io.get_word_embeddings_path(layer), data.numpy(), sep=",")


def save_document_embeddings(data, layer):
    io.write_csv(io.get_document_embeddings_path(layer), data.numpy(), sep=",")


# Dataset
def get_cleaned_sentences(dataset=FLAGS.dataset):
    path = io.get_clean_sentences_path(dataset)
    exist(path, "Your dataset must include a `_cleaned_sentences.txt` file")
    return io.read_txt(path)


def get_sentences(dataset=FLAGS.dataset):
    path = io.get_sentences_path(dataset)
    exist(path, "Your dataset must include a `_sentences.txt` file")
    return io.read_txt(path)


def get_labels(dataset=FLAGS.dataset):
    path = io.get_labels_path(dataset)
    exist(path, "Your dataset must include a `_labels.txt` file")
    return io.read_txt(path)


def get_vocab(dataset=FLAGS.dataset):
    path = io.get_vocab_path(dataset)
    exist(path, "Your dataset must include a `_vocab.txt` file")
    return io.read_txt(path)


def save_clean_sentences(data, dataset=FLAGS.dataset):
    io.write_txt(data, io.get_clean_sentences_path(dataset))


def save_vocab(data, dataset=FLAGS.dataset):
    io.write_txt(data, io.get_vocab_path(dataset))


def save_sentences(data, dataset=FLAGS.dataset):
    io.write_txt(data, io.get_sentences_path(dataset))


def save_labels(data, dataset=FLAGS.dataset):
    io.write_txt(data, io.get_labels_path(dataset))


# Nouns

def get_nouns(dataset=FLAGS.dataset):
    path = io.get_nouns_path(dataset)
    exist(path, "Dataset has not been tokenized yet, run `prep_data.py`")
    return io.read_txt(path)


def get_normalized_nouns(dataset=FLAGS.dataset):
    path = io.get_normalized_nouns_path(dataset)
    exist(path, "Dataset has not been tokenized yet, run `prep_data.py`")
    return io.read_txt(path)


def get_nouns_vocab(dataset=FLAGS.dataset):
    path = io.get_nouns_vocab(dataset)
    exist(path, "Dataset has not been tokenized yet, run `prep_data.py`")
    return io.read_txt(path)


def save_nouns(data, dataset=FLAGS.dataset):
    io.write_txt(data, io.get_nouns_path(dataset))


def save_normalized_nouns(data, dataset=FLAGS.dataset):
    io.write_txt(data, io.get_normalized_nouns_path(dataset))


def save_nouns_vocab(data, dataset=FLAGS.dataset):
    io.write_txt(data, io.get_nouns_vocab(dataset))


# WikiData Entities & Relations
def get_entity2id(dataset=FLAGS.dataset):
    return io.read_csv(io.get_entity2id_path(dataset), sep=",")


def save_entity2id(data, dataset=FLAGS.dataset):
    io.write_csv(io.get_entity2id_path(dataset), data, sep=",", header=["word", "wikiID"])


def get_doc2id(dataset=FLAGS.dataset):
    return io.read_csv(io.get_doc2id_path(dataset), sep=",")


def save_doc2id(data, dataset=FLAGS.dataset):
    io.write_csv(io.get_doc2id_path(dataset), data, sep=",", header=["doc", "wikiID"])


def get_doc2relations(dataset=FLAGS.dataset):
    return io.read_txt(io.get_doc2relations_path(dataset))


def save_doc2relations(data, dataset=FLAGS.dataset):
    io.write_txt(data, io.get_doc2relations_path(dataset))


def get_doc2idf(dataset=FLAGS.dataset):
    return io.read_csv(io.get_doc2idf_path(dataset), sep=",")


def save_doc2idf(data, dataset=FLAGS.dataset):
    io.write_csv(io.get_doc2idf_path(dataset), data, sep=",", header=["doc", "relation", "idf", "idf_wiki"])


def get_vocab_entities(dataset=FLAGS.dataset):
    return io.read_json(io.get_vocab_entities_path(dataset))


def get_vocab_relations(dataset=FLAGS.dataset):
    return io.read_json(io.get_vocab_relations_path(dataset))


def save_vocab_entities(data, dataset=FLAGS.dataset):
    io.write_json(io.get_vocab_entities_path(dataset), data)


def save_vocab_relations(data, dataset=FLAGS.dataset):
    io.write_json(io.get_vocab_relations_path(dataset), data)


# WikiData Relations
def get_filtered_relations():
    path = io.get_filtered_wiki_relations_path()
    exist(path, "Run `analyze_properties.py` to generate this file")
    return io.read_csv(path, sep="\n")["ID"].tolist()


def save_filtered_relations(data):
    io.write_csv(io.get_filtered_wiki_relations_path(), data, sep="+", header=["ID"])


def get_all_relations():
    path = io.get_all_wiki_relations_path()
    exist(path, "Run `analyze_properties.py` to generate this file")
    return io.read_csv(path, sep="+")


def save_all_relations(data):
    io.write_csv(io.get_all_wiki_relations_path(), data, sep="+",
                 header=["ID", "label", "description", "aliases", "type", "count"])


# Triples
def get_all_triples(dataset=FLAGS.dataset):
    return io.read_csv(io.get_all_word_triples_path(dataset), sep=",")


def save_all_triples(data, dataset=FLAGS.dataset):
    io.write_csv(io.get_all_word_triples_path(dataset), data, sep=",", header=["entity1", "relation", "entity2"])


def get_filtered_triples(dataset=FLAGS.dataset):
    return io.read_csv(io.get_filtered_word_triples_path(dataset), sep=",")


def save_filtered_triples(data, dataset=FLAGS.dataset):
    io.write_csv(io.get_filtered_word_triples_path(dataset), data, sep=",", header=["entity1", "relations", "entity2"])


def get_document_triples(dataset=FLAGS.dataset):
    path = io.get_document_triples_path(dataset)
    exist(path, "Document triples do not exist yet.")
    return io.read_pickle(path)


def save_document_triples(data, dataset=FLAGS.dataset):
    path = io.get_document_triples_path(dataset)
    io.write_pickle(path, data)
    csv_path = path.replace(".pickle.bz2", ".csv")
    io.write_csv(csv_path, data, sep=",", header=["doc1", "doc2", "relations", "detail"])


def get_document_triples_metrics(dataset=FLAGS.dataset):
    path = io.get_document_triples_metrics_path(dataset)
    exist(path, "Document triples metrics do not exist yet.")
    return io.read_pickle(path)


def save_document_triples_metrics(data, dataset=FLAGS.dataset):
    path = io.get_document_triples_metrics_path(dataset)
    io.write_pickle(path, data)
    csv_path = path.replace(".pickle.bz2", ".csv")
    io.write_csv(csv_path, data, sep=",", header=["doc1", "doc2", "count", "idf", "idf_wiki"])


# Evaluation logger
def get_eval_logs(dataset=FLAGS.dataset):
    path = io.get_eval_log_path(dataset)
    if not exists(path):
        return None
    return io.read_csv(path, sep=';')


def save_eval_logs(data, dataset=FLAGS.dataset):
    io.write_csv(io.get_eval_log_path(dataset), data, sep=';')


def save_result_log(data, dataset=FLAGS.dataset):
    io.write_json(io.get_result_log_path(dataset), data)


# Helper
def exist(path, error):
    if not exists(path):
        raise ValueError(error)


def check_files():
    exist(io.get_document_triples_path(),
                 "To run textKGCN you need a file with doc2doc edges. Run `prep_graph.py` to create all needed files.")
