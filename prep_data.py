import re
from collections import defaultdict
from os.path import exists
import nltk
from nltk.corpus import stopwords
import io_utils as io
import file_utils as file


def clean_data(dataset):
    clean_text_path = io.get_clean_sentences_path(dataset)
    if not exists(clean_text_path):
        old_name = dataset
        docs_list = file.get_sentences(dataset)
        dataset = old_name
        word_counts = defaultdict(int)
        for doc in docs_list:
            temp = clean_doc(doc)
            words = temp.split()
            for word in words:
                word_counts[word] += 1
        clean_docs = clean_documents(docs_list, word_counts)
        corpus_str = '\n'.join(clean_docs)
        f = open(clean_text_path, 'w')
        f.write(corpus_str)
        f.close()
    f = open(clean_text_path, 'r')
    lines = f.readlines()
    min_len = 10000
    aver_len = 0
    max_len = 0
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


def clean_documents(docs, word_counts):
    nltk.download('stopwords')
    stop_words = set(stopwords.words('english'))
    print(stop_words)
    ret = []
    for doc in docs:
        doc = clean_doc(doc)
        words = doc.split()
        words = [word for word in words if word not in stop_words and word_counts[word] >= 5]
        doc = ' '.join(words).strip()
        if doc != '':
            ret.append(' '.join(words).strip())
        else:
            ret.append(' ')
    return ret


def clean_doc(string):
    string = re.sub(r"^\"", "", string)
    string = re.sub(r"\"$", "", string)
    string = re.sub(r"\'s", " \'s", string)
    string = re.sub(r"\'ve", " \'ve", string)
    string = re.sub(r"n\'t", " n\'t", string)
    string = re.sub(r"\'re", " \'re", string)
    string = re.sub(r"\'d", " \'d", string)
    string = re.sub(r"\'ll", " \'ll", string)
    string = re.sub(r"\.", " ", string)
    string = re.sub(r",", " ", string)
    string = re.sub(r"!", " ", string)
    string = re.sub(r"\(", " ", string)
    string = re.sub(r"\)", " ", string)
    string = re.sub(r"\?", " ", string)
    string = re.sub(r"\s{2,}", " ", string)
    return string.strip().lower()
