from os.path import join

from idna import unicode

from helper import io_utils as io, file_utils


def prep_ohsumed():
    # Source: https://github.com/yao8839836/text_gcn
    corpus_path = io.get_corpus_path("ohsumed")

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
    io.write_txt(label_file, join(corpus_path, "ohsumed_labels.txt"))
    io.write_txt(sentences_file, join(corpus_path, "ohsumed_sentences.txt"))


def prep_r52():
    # Source: https://www.cs.umb.edu/~smimarog/textmining/datasets/
    read("r52")


def prep_20ng():
    # Source: https://www.cs.umb.edu/~smimarog/textmining/datasets/
    read("20ng")


def prep_mr():
    # Source: https://github.com/yao8839836/text_gcn
    data = []
    sentences = file_utils.get_sentences()
    print(sentences[0:10])
    import unicodedata

    # try:
    #     text = unicode(sentences, 'utf-8')
    # except NameError:  # unicode is a default on python 3
    #     pass
    for s in sentences:
        text = unicodedata.normalize('NFD', s) \
            .encode('ascii', 'ignore') \
            .decode("utf-8")
        string = str(text)
        data.append(string)

    # file = open(join(io.get_corpus_path("mr"), "mr_sentences1.txt"), 'r')
    # # content = file.read()
    # # print(content)
    # for line in file.readlines():
    #     data.append(line)
    # file.close()
    # io.read_txt(join(io.get_corpus_path("mr"), "mr_sentences1.txt"))

    file_utils.save_sentences(data)


def read(name):
    corpus_path = io.get_corpus_path(name)
    test_data = io.read_txt(join(corpus_path, f"{name}-test-stemmed.txt"))
    train_data = io.read_txt(join(corpus_path, f"{name}-train-stemmed.txt"))
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

    io.write_txt(label_file, join(corpus_path, f"{name}_labels.txt"))
    io.write_txt(sentences_file, join(corpus_path, f"{name}_sentences.txt"))


if __name__ == '__main__':
    prep_mr()