import re
import nltk
from nltk.corpus import stopwords
from config import FLAGS
from generate_nouns import generate_nouns
from helper import io_utils as io, file_utils as file


def clean_data():
    dataset = FLAGS.dataset
    nltk.download('stopwords')
    stop_words = set(stopwords.words('english'))

    doc_content_list = []
    f = open(io.get_sentences_path(dataset), "rb")

    for line in f.readlines():
        doc_content_list.append(line.strip().decode('latin1'))
    f.close()

    word_freq = {}  # to remove rare words

    for doc_content in doc_content_list:
        temp = clean_str(doc_content)
        words = temp.split()
        for word in words:
            if word in word_freq:
                word_freq[word] += 1
            else:
                word_freq[word] = 1

    clean_docs = []
    for doc_content in doc_content_list:
        temp = clean_str(doc_content)
        words = temp.split()
        doc_words = []
        for word in words:
            # word not in stop_words and word_freq[word] >= 5
            if dataset == 'mr':
                doc_words.append(word)
            elif word not in stop_words and word_freq[word] >= 5:
                doc_words.append(word)

        doc_str = ' '.join(doc_words).strip()
        clean_docs.append(doc_str)

    clean_corpus_str = '\n'.join(clean_docs)

    f = open(io.get_clean_sentences_path(dataset), 'w')
    f.write(clean_corpus_str)
    f.close()

    min_len = 10000
    aver_len = 0
    max_len = 0

    f = open(io.get_clean_sentences_path(), 'r')

    lines = f.readlines()
    for line in lines:
        line = line.strip()
        temp = line.split()
        aver_len = aver_len + len(temp)
        if len(temp) < min_len:
            min_len = len(temp)
        if len(temp) > max_len:
            max_len = len(temp)
    f.close()
    aver_len = 1.0 * aver_len / len(lines)
    print('min_len : ' + str(min_len))
    print('max_len : ' + str(max_len))
    print('average_len : ' + str(aver_len))

    create_vocab(dataset)
    generate_nouns(dataset)


def clean_str(string):
    """
    Tokenization/string cleaning for all datasets except for SST.
    Original taken from https://github.com/yoonkim/CNN_sentence/blob/master/process_data.py
    """
    string = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", string)
    string = re.sub(r"\'s", " \'s", string)
    string = re.sub(r"\'ve", " \'ve", string)
    string = re.sub(r"n\'t", " n\'t", string)
    string = re.sub(r"\'re", " \'re", string)
    string = re.sub(r"\'d", " \'d", string)
    string = re.sub(r"\'ll", " \'ll", string)
    string = re.sub(r",", " , ", string)
    string = re.sub(r"!", " ! ", string)
    string = re.sub(r"\(", " \( ", string)
    string = re.sub(r"\)", " \) ", string)
    string = re.sub(r"\?", " \? ", string)
    string = re.sub(r"\s{2,}", " ", string)
    return string.strip().lower()


def create_vocab(dataset):
    # Vocabulary and sentences
    vocabs = []
    sentences_clean = file.get_cleaned_sentences()

    for line in sentences_clean:
        # Vocabulary
        words = line.split(sep=" ")
        vocabs += words

    # Make vocabs unique
    unique_vocab = list(dict.fromkeys(vocabs))

    # Save to new file
    file.save_vocab(unique_vocab, dataset)


if __name__ == '__main__':
    clean_data()

