from helper import file_utils as file
from prep_data import clean_data


def create_small_dataset(dataset, size=300):
    new_datatset = f'{dataset}_small'

    # Load files
    sentences = file.get_sentences(dataset)
    labels = file.get_labels(dataset)

    # Sentences & Labels
    sentences_normal = sentences[0:size]
    doc_labels = list(map(lambda label: label.split(sep="\t")[2], labels[0:size]))

    clean_data(new_datatset)

    file.save_sentences(sentences_normal, new_datatset)
    file.save_labels(doc_labels, new_datatset)

    print(f"Small dataset created with {size} documents (based on: {dataset})")


if __name__ == '__main__':
    create_small_dataset("r8")
