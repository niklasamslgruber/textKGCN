import io_utils as io


def create_small_dataset(dataset, size=300):
    new_datatset = f'{dataset if "presplit" not in dataset else dataset.replace("_presplit", "")}_small'

    # Load files
    cleaned_sentences = io.read_txt(io.get_clean_sentences_path(dataset))
    sentences = io.read_txt(io.get_sentences_path(dataset))
    labels = io.read_txt(io.get_labels_path(dataset))

    # Sentences & Labels
    sentences_normal = sentences[0:size]
    doc_labels = list(map(lambda label: label.split(sep="\t")[2], labels[0:size]))

    # Vocabulary and sentences
    vocabs = []
    sentences_clean = cleaned_sentences[0:size]

    for line in sentences_clean:
        # Vocabulary
        words = line.split(sep=" ")
        vocabs += words

    # Make vocabs unique
    unique_vocab = list(dict.fromkeys(vocabs))

    # Save to new file
    assert len(sentences_normal) == len(sentences_clean) == len(doc_labels)

    io.write_txt(sentences_normal, io.get_sentences_path(new_datatset))
    io.write_txt(unique_vocab, io.get_vocab_path(new_datatset))
    io.write_txt(sentences_clean, io.get_clean_sentences_path(new_datatset))
    io.write_txt(doc_labels, io.get_labels_path(new_datatset))

    print(f"Small dataset created with {size} documents (based on: {dataset})")


if __name__ == '__main__':
    create_small_dataset("r8_presplit")
