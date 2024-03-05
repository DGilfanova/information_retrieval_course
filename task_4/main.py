import math
import json
from pymorphy3 import MorphAnalyzer
import zipfile
import re
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk

# Перед запуском необходимо установить библиотеки: pip3 install pymorphy2 nltk

parser = 'html.parser'
morph = MorphAnalyzer()
ZIP_FILE_PATH = "pages.zip"
INVERTED_INDEX_FILE = 'inverted_index.txt'
TOKENS_TFIDF_DIR = 'tf-idf/tokens/'
LEMMAS_TFIDF_DIR = 'tf-idf/lemmas/'


def extract_unique_filtered_tokens(tokens):
    res = []
    for token in tokens:
        if token.lower() not in stopwords.words("russian") and re.compile("^[а-яё]+$").match(token.lower()):
            res.append(token.lower())
    return set(res)


def tokenize(text):
    tokens = word_tokenize(text.replace('.', ' '))
    return extract_unique_filtered_tokens(tokens)


def get_inverted_index_tokens(zip_file):
    index = {}

    for i, file in enumerate(zip_file.filelist):
        content = zip_file.open(file)
        text = BeautifulSoup(content, parser).get_text()
        tokens = set(tokenize(text))

        for token in tokens:
            if token in index:
                index[token].add(i)
            else:
                index[token] = {i}
    return index


def list_extract_unique_filtered_tokens(tokens):
    res = []
    for token in tokens:
        if token.lower() not in stopwords.words("russian") and re.compile("^[а-яё]+$").match(token.lower()):
            res.append(token.lower())
    return list(res)


def get_tokens(text):
    tokens = word_tokenize(text.replace('.', ' '))
    return list_extract_unique_filtered_tokens(tokens)

def read_lemmas():
    lemmas = {}
    with open(INVERTED_INDEX_FILE, 'r', encoding='utf-8') as file:
        for line in file.readlines():
            res = json.loads(line)
            lemmas[res['word']] = res['inverted_array']
    return lemmas

def calculate_tf(q, tokens):
    return tokens.count(q) / float(len(tokens))


def calculate_idf(q, index, docs_count=100):
    return math.log(docs_count / float(len(index[q])))


def lemmatize(word):
    return morph.parse(word.replace("\n", ""))[0].normal_form


def calculate_tfidf(zip_file, lemmas_index, tokens_index):
    for i, file in enumerate(zip_file.filelist):
        content = zip_file.open(file)
        text = BeautifulSoup(content, parser).get_text()

        tokens = get_tokens(text)
        lemmas = list(map(lemmatize, tokens))

        res_tokens = []
        for token in set(tokens):
            if token in tokens_index:
                tf = calculate_tf(token, tokens)
                idf = calculate_idf(token, tokens_index)
                res_tokens.append(f"{token} {idf} {tf * idf}")

        with open(f"{TOKENS_TFIDF_DIR}{file.filename.replace('.html','')}.txt", "w", encoding='utf-8') as token_f:
            token_f.write("\n".join(res_tokens) + ',')

        res_lemmas = []
        for lemma in set(lemmas):
            if lemma in lemmas_index:
                tf = calculate_tf(lemma, lemmas)
                idf = calculate_idf(lemma, lemmas_index)
                res_lemmas.append(f"{lemma} {idf} {tf * idf}")

        with open(f"{LEMMAS_TFIDF_DIR}{file.filename.replace('.html','')}.txt", "w", encoding='utf-8') as lemma_f:
            lemma_f.write("\n".join(res_lemmas))


def main():
    nltk.download('punkt')
    nltk.download('stopwords')

    zip_file = zipfile.ZipFile(ZIP_FILE_PATH, "r")

    inverted_index_tokens = get_inverted_index_tokens(zip_file)

    read_inverted_index = read_lemmas()

    calculate_tfidf(zip_file, read_inverted_index, inverted_index_tokens)


if __name__ == '__main__':
    main()
