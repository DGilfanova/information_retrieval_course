from bs4 import BeautifulSoup
import nltk
import os
import re
from pymorphy2 import MorphAnalyzer
from nltk.corpus import stopwords
from collections import defaultdict

# Перед запуском необходимо установить библиотеки: pip3 install nltk pymorphy2


def tokenize(text, stop_words):
    tokens = [token.lower() for token in nltk.word_tokenize(text)]

    # очищаем от стоп-слов, оставляем только русские слова и приводим к нижнему регистру
    return [token for token in tokens if token.isalpha() and token not in stop_words and bool(re.match(r'^[А-Яа-я]+$', token))]


def extract_text_from_html(html_doc):
    soup = BeautifulSoup(html_doc, 'html.parser')
    text = soup.get_text()
    return text


def group_tokens_by_lemma(tokens, lemmatizer):
    lemma_groups = defaultdict(list)
    for token in tokens:
        lemma = lemmatizer.parse(token)[0].normal_form
        lemma_groups[lemma].append(token)
    return lemma_groups


def main():
    # Считаем, что все html файлы выгружены в папку task_2
    html_folder = '/Users/d.gilfanova/PycharmProjects/information_retrieval_course/task_2'
    all_tokens = set()
    lemma_token_groups = defaultdict(list)

    lemmatizer = MorphAnalyzer()
    stop_words = set(stopwords.words('russian'))

    nltk.download('wordnet')
    nltk.download('stopwords')
    nltk.download('punkt')

    for filename in os.listdir(html_folder):
        if filename.endswith('.html'):
            with open(os.path.join(html_folder, filename), 'r', encoding='utf-8') as file:
                html_doc = file.read()
                text = extract_text_from_html(html_doc)
                tokens = tokenize(text, stop_words)
                all_tokens.update(tokens)

    lemma_groups = group_tokens_by_lemma(all_tokens, lemmatizer)
    for lemma, group in lemma_groups.items():
        lemma_token_groups[lemma].extend(group)

    with open('tokens_1.txt', 'w', encoding='utf-8') as file:
        for token in sorted(all_tokens):
            file.write(f"{token}\n")

    with open('lemma_1.txt', 'w', encoding='utf-8') as file:
        for lemma, tokens in sorted(lemma_token_groups.items()):
            file.write(f"{lemma}: {' '.join(sorted(set(tokens)))}\n")


if __name__ == "__main__":
    main()
