from os.path import join
from utils import get_data_path, get_corpus_path


# Readers
def get_base_path(dataset):
    return join(get_corpus_path(), dataset)


def get_base_data(dataset):
    base_path = get_base_path(dataset)
    clean_sentences_path = base_path + '_sentences_clean.txt'
    sentences_path = base_path + '_sentences.txt'
    labels_path = base_path + '_labels.txt'

    return clean_sentences_path, sentences_path, labels_path


def write_to_txt(data, path):
    f = open(path, 'w')
    f.writelines("\n".join(data))
    f.close()


def create_small_dataset(dataset, size=300):
    clean_sentences_path, sentences_path, labels_path = get_base_data(dataset)

    small_dataset_name = dataset if "presplit" not in dataset else dataset.replace("_presplit", "")
    print(small_dataset_name)

    # Load files
    cleaned_sentences = open(clean_sentences_path, 'r')
    sentences = open(sentences_path, 'r')
    labels = open(labels_path, 'r')
    base_path = join(get_corpus_path(), small_dataset_name)

    # Vocabulary and sentences
    vocabs = []
    sentences_clean = []

    for line in cleaned_sentences.readlines()[0:size]:
        # Cleaned sentences
        sentence = line.replace("\n", "")
        sentences_clean.append(sentence)

        # Vocabulary
        words = sentence.split(sep=" ")
        filtered_words = map(lambda word: word.replace("\n", ""), words)
        vocabs += filtered_words

    # Make vocabs unique
    unique_vocab = list(dict.fromkeys(vocabs))

    # Sentences
    sentences_normal = []
    for line in sentences.readlines()[0:size]:
        doc = line.replace("\n", "")
        sentences_normal.append(doc)

    # Labels
    doc_labels = []
    for line in labels.readlines()[0:size]:
        label = line.split(sep="\t")[2].replace("\n", "")
        doc_labels.append(label)

    # Close files
    labels.close()
    sentences.close()
    cleaned_sentences.close()

    # Save to new file
    assert len(sentences_normal) == len(sentences_clean) == len(doc_labels)
    write_to_txt(sentences_normal, base_path + "_small_sentences.txt")
    write_to_txt(unique_vocab, base_path + "_small_vocab.txt")
    write_to_txt(sentences_clean, base_path + "_small_sentences_clean.txt")
    write_to_txt(doc_labels, base_path + "_small_labels.txt")

    print(f"Small dataset created with {size} documents (based on: {dataset})")


if __name__ == '__main__':
    create_small_dataset("r8_presplit")
