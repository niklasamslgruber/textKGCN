import file_utils as file


def create_small_dataset(dataset, size=300):
    new_datatset = f'{dataset if "presplit" not in dataset else dataset.replace("_presplit", "")}_small'

    # Load files
    cleaned_sentences = file.get_cleaned_sentences(dataset)
    sentences = file.get_sentences(dataset)
    labels = file.get_labels(dataset)

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

    file.save_sentences(sentences_normal, new_datatset)
    file.save_vocab(unique_vocab, new_datatset)
    file.save_clean_sentences(sentences_clean, new_datatset)
    file.save_labels(doc_labels, new_datatset)

    print(f"Small dataset created with {size} documents (based on: {dataset})")


if __name__ == '__main__':
    create_small_dataset("r8_presplit")
