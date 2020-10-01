import io_utils as io


def write_to_txt(data, path):
    f = open(path, 'w')
    f.writelines("\n".join(data))
    f.close()


def create_small_dataset(dataset, size=300):
    small_dataset_name = dataset if "presplit" not in dataset else dataset.replace("_presplit", "")
    small_dataset_name += "_small"

    # Load files
    cleaned_sentences = open(io.get_clean_sentences_path(dataset), 'r')
    sentences = open(io.get_sentences_path(dataset), 'r')
    labels = open(io.get_labels_path(dataset), 'r')

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

    write_to_txt(sentences_normal, io.get_sentences_path(small_dataset_name))
    write_to_txt(unique_vocab, io.get_vocab_path(small_dataset_name))
    write_to_txt(sentences_clean, io.get_clean_sentences_path(small_dataset_name))
    write_to_txt(doc_labels, io.get_labels_path(small_dataset_name))

    print(f"Small dataset created with {size} documents (based on: {dataset})")


if __name__ == '__main__':
    create_small_dataset("r8_presplit")
