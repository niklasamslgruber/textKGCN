import spacy
from helper import file_utils as file
from tqdm import tqdm

# Helper
# lemmas = [token.lemma_ for token in doc]
# words = [token.text for token in doc]
# tags = [token.tag_ for token in doc]
# pos = [token.pos_ for token in doc]
# [(ent.text, ent.label_) for ent in doc.ents]

nlp = spacy.load("en")


def extract_nouns(text):
    doc = nlp(text)
    nouns = []
    normalized_nouns = []
    for token in doc:
        if token.pos_ == "NOUN":
            normalized_nouns.append(token.lemma_)
            nouns.append(token.text)

    return nouns, normalized_nouns


def generate_nouns(dataset):
    clean_sentences = file.get_cleaned_sentences(dataset)
    doc_nouns = []
    doc_nouns_normalized = []
    print("Starting to generate nouns")
    for sent in tqdm(clean_sentences):
        nouns, normalized_nouns = extract_nouns(sent)
        nouns = list(set(nouns))
        normalized_nouns = list(set(normalized_nouns))

        doc_nouns.append(" ".join(nouns))
        doc_nouns_normalized.append(" ".join(normalized_nouns))

    file.save_nouns(doc_nouns)
    file.save_normalized_nouns(doc_nouns_normalized)
    create_normalized_vocab()


def create_normalized_vocab():
    normalized_nouns = file.get_normalized_nouns()
    vocabs = []
    print("Starting to create normalized vocab")
    for line in tqdm(normalized_nouns):
        # Vocabulary
        words = line.split(sep=" ")
        while "" in words:
            words.remove("")
        vocabs += words

        # Make vocabs unique
    unique_vocab = list(dict.fromkeys(vocabs))
    file.save_nouns_vocab(unique_vocab)