from helper import io_utils as io, file_utils as file
import pandas as pd

def load_20ng():
    path = io.get_root_path() + "/data/20ng.txt"
    files = io.read_txt(path)
    labels = []
    sents = []
    for index, x in enumerate(files):
        cats = x.split("\t")
        if "20news-bydate-test" in cats:
            cats[1] = "test"
        elif "20news-bydate-train" in cats:
            cats[1] = "train"

        with open(cats[0], "rt") as f:
            sentence = f.readlines()
            sentence = [sen.replace("\n", " ") for sen in sentence]
            sentence = [sen.replace("\t", " ") for sen in sentence]
            sentences = " ".join(sentence)
        f.close()

        labels.append("\t".join([str(index), cats[1], cats[2]]))
        sents.append(sentences)

    file.save_labels(labels, "20ng")
    file.save_sentences(sents, "20ng")


def load_ohsumed():
    path = io.get_root_path() + "/data/ohsumed.txt"
    files = io.read_txt(path)
    labels = []
    sents = []
    for index, x in enumerate(files):
        cats = x.split("\t")
        if "training" in cats[1]:
            cats[1] = "train"

        with open(cats[0], "rt") as f:
            sentence = f.readlines()
            sentence = [sen.replace("\n", " ") for sen in sentence]
            sentence = [sen.replace("\t", " ") for sen in sentence]
            sentences = " ".join(sentence)
        f.close()

        labels.append("\t".join([str(index), cats[1], cats[2]]))
        sents.append(sentences)

    file.save_labels(labels, "ohsumed")
    file.save_sentences(sents, "ohsumed")


def load_mr():
    path = io.get_root_path() + "/mr_dataset/mr.txt"
    text_file = io.get_root_path() + "/mr_dataset/mr/text_all.txt"
    files = io.read_txt(path)
    labels = []
    sents = []

    all_sents = []
    with open(text_file, "r", encoding="iso-8859-1") as f:
        all_sents = f.readlines()
    f.close()

    for index, x in enumerate(files):
        cats = x.split("\t")

        sentences = all_sents[index].replace("\n", " ").replace("\t", " ")
        sentences = strip_accents(sentences)
        labels.append("\t".join([str(index), cats[1], cats[2]]))
        sents.append(sentences)

    file.save_labels(labels, "mr")
    file.save_sentences(sents, "mr")


def strip_accents(text):
    import unidecode
    unaccented_string = unidecode.unidecode(text)
    return unaccented_string


def load_r52():
    path = io.get_root_path() + "/data/R52.txt"

    train_set = io.get_root_path() + "/data/train.txt"
    test_set = io.get_root_path() + "/data/test.txt"

    labels_file = io.get_root_path() + "/data/R52_labels.txt"
    unique = []
    with open(labels_file, "r") as f:
        unique = f.readlines()
    f.close()
    unique = [x.replace("\n", "") for x in unique]
    print(unique)

    all_labels = []
    with open(path, "r") as f:
        all_labels = f.readlines()
    f.close()

    all_train = []
    with open(train_set, "r") as f:
        all_train = f.readlines()
        all_train = [x.replace("\t", " ").replace("\n", "") for x in all_train]
    print(all_train[0])
    f.close()
    all_train = [x.split(" ", maxsplit=1)[1] for x in all_train]

    all_test = []
    with open(test_set, "r") as f:
        all_test = f.readlines()
        all_test = [x.replace("\t", " ").replace("\n", "") for x in all_test]
    f.close()

    all_test = [x.split(" ", maxsplit=1)[1] for x in all_test]

    all_docs = all_train + all_test
    file.save_labels(all_labels, "r52")
    file.save_sentences(all_docs, "r52")


if __name__ == '__main__':
    load_mr()

