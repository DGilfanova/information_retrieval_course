import nltk
import json
import os
from bs4 import BeautifulSoup
from pymorphy2 import MorphAnalyzer
from pyparsing import Word, Suppress, Group, Forward, srange, CaselessLiteral, ZeroOrMore

# Перед запуском необходимо установить библиотеки: pip3 install pyparsing


def read_lemmas_from_file(file_path):
    lemmas_dict = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            lemma, tokens_str = line.strip().split(': ')
            tokens = tokens_str.split()
            for token in tokens:
                lemmas_dict[token] = lemma
    return lemmas_dict


def build_index_from_html_files(html_files_dir, lemmas_dir):
    index = {}
    for doc_i in range(1, 111):
        file_path = os.path.join(html_files_dir, f'{doc_i}.html')
        with open(file_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')
            text = soup.get_text()
            words = [token.lower() for token in nltk.word_tokenize(text)]
            for word in words:
                lemma = lemmas_dir.get(word)
                if lemma:
                    if lemma not in index:
                        index[lemma] = {'count': 0, 'inverted_array': []}
                    if doc_i not in index[lemma]['inverted_array']:
                        index[lemma]['inverted_array'].append(doc_i)
                        index[lemma]['count'] += 1
    return index


def save_index_to_file(index, index_file_name):
    with open(index_file_name, 'w', encoding='utf-8') as file:
        for key, value in index.items():
            count = value['count']
            array = value['inverted_array']
            file.write(f'{{"word":"{key}", "count":{count},"inverted_array":{array}}}\n')


def search(index, query, lemmatizer):
    AND, OR, NOT = map(CaselessLiteral, ["AND", "OR", "NOT"])
    term = Word(srange("[а-яА-Я]"))

    expr = Forward()
    atom = (NOT + term | term | NOT + Group(Suppress("(") + expr + Suppress(")")) | Group(Suppress("(") + expr + Suppress(")")))
    clause = Group(atom + ZeroOrMore(AND + atom | OR + atom))
    expr <<= clause

    def interpret_expr(query, index):
        if isinstance(query, str):
            token = lemmatizer.parse(query.lower())[0].normal_form
            return index.get(token)
        elif query[0] == "NOT":
            not_docs = interpret_expr(query[1], index)
            all_docs = set(range(1, len(index) + 1))
            return list(all_docs - set(not_docs))
        else:
            result = interpret_expr(query[0], index)
            for op, term in zip(query[1::2], query[2::2]):
                term_docs = interpret_expr(term, index)
                if op == "AND":
                    result = list(set(result) & set(term_docs))
                elif op == "OR":
                    result = list(set(result) | set(term_docs))
            return result

    parsed_query = expr.parseString(query)[0]
    return interpret_expr(parsed_query, index)


def create_index(index_file_name):
    lemmas_dir = read_lemmas_from_file('lemma_1.txt')
    # В pages хранятся все выгруженные html-странички
    index = build_index_from_html_files('/pages', lemmas_dir)
    save_index_to_file(index, index_file_name)


def get_index(index_file_name):
    index = {}
    with open(index_file_name, 'r', encoding='utf-8') as file:
        for line in file:
            data = json.loads(line)
            word = data['word']
            index[word] = data['inverted_array']
    return index


def main():
    index_file_name = 'inverted_index.txt'
    # Вызываем единожды для создания inverted_index.txt файла
    # create_index(index_file_name)

    index = get_index(index_file_name)
    lemmatizer = MorphAnalyzer()

    while True:
        query = input("Введите запрос: ")
        try:
            results = search(index, query, lemmatizer)
            print("Результаты поиска:", results)
        except Exception:
            print("Не найдено")


if __name__ == "__main__":
    main()
