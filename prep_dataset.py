from os.path import join
from helper import io_utils as io


def prep_ohsumed():
    # Source: https://github.com/yao8839836/text_gcn
    corpus_path = io.get_corpus_path("ohsumed_presplit")

    labels_data = io.read_txt(join(corpus_path, "ohsumed.txt"))
    label_file = []
    sentences_file = []

    for index, data in enumerate(labels_data):
        arr = data.split("\t")
        path = arr[0]
        data_type = arr[1]
        model_type = "test" if data_type == "test" else "train"
        label = arr[2]
        file = open(join(corpus_path, path), "rb")
        sentence = file.read().decode().replace("\n", "")
        label_file.append("\t".join([str(index), model_type, label]))
        sentences_file.append(sentence)

    assert len(label_file) == len(sentences_file) == len(labels_data)
    print(label_file[0:2])
    print(sentences_file[0:2])
    io.write_txt(label_file, join(corpus_path, "ohsumed_presplit_labels.txt"))
    io.write_txt(sentences_file, join(corpus_path, "ohsumed_presplit_sentences.txt"))


def prep_mr():
    # Source: https://github.com/yao8839836/text_gcn
    corpus_path = io.get_corpus_path("mr")
    print(corpus_path)
    print(join(corpus_path, f"mr_sentences.txt"))
    test_data = io.read_txt(join(corpus_path, f"mr/text_all.txt"))
    io.write_txt(test_data, join(corpus_path, f"mr_presplit_sentences.txt"))


def prep_r52():
    # Source: https://www.cs.umb.edu/~smimarog/textmining/datasets/
    read("r52", "r52_presplit")


def prep_20ng():
    # Source: https://www.cs.umb.edu/~smimarog/textmining/datasets/
    read("20ng", "20ng_presplit")


def read(read_name, out_file):
    corpus_path = io.get_corpus_path(out_file)
    test_data = io.read_txt(join(corpus_path, f"{read_name}-test-stemmed.txt"))
    train_data = io.read_txt(join(corpus_path, f"{read_name}-train-stemmed.txt"))
    data = train_data + test_data

    label_file = []
    len_train = len(train_data)
    print(len(train_data))
    sentences_file = []
    for index, test_item in enumerate(data):
        desc = "train" if index < len_train else "test"
        data_array = test_item.split("\t")
        label = data_array[0]
        sentence = data_array[1]
        label_file.append("\t".join([str(index), desc, label]))
        sentences_file.append(sentence)

    assert len(label_file) == len(sentences_file)

    io.write_txt(label_file, join(corpus_path, f"{out_file}_labels.txt"))
    io.write_txt(sentences_file, join(corpus_path, f"{out_file}_sentences.txt"))
