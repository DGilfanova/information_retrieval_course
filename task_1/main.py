import requests
import zipfile
from bs4 import BeautifulSoup
import os
import re

# Перед запуском необходимо установить библиотеки: pip install requests beautifulsoup4

urls = [
    'https://news.un.org/ru/story/2024/02/1449562',
    'https://news.un.org/ru/story/2024/02/1449612',
    'https://news.un.org/ru/story/2024/02/1449567',
    'https://news.un.org/ru/story/2024/02/1449607',
    'https://news.un.org/ru/story/2024/02/1449527',
    'https://news.un.org/ru/story/2024/02/1449322',
    'https://news.un.org/ru/story/2024/02/1449422',
    'https://news.un.org/ru/story/2024/02/1449237',
    'https://news.un.org/ru/story/2024/01/1448572',
    'https://news.un.org/ru/story/2024/02/1449042',
    'https://news.un.org/ru/story/2023/12/1447347',
    'https://news.un.org/ru/story/2023/11/1447277',
    'https://news.un.org/ru/story/2024/02/1449337',
    'https://news.un.org/ru/story/2024/01/1449077',
    'https://news.un.org/ru/story/2024/01/1448922',
    'https://news.un.org/ru/story/2024/01/1448927',
    'https://news.un.org/ru/story/2023/12/1447752',
    'https://news.un.org/ru/story/2024/02/1449547',
    'https://news.un.org/ru/story/2024/02/1449542',
    'https://news.un.org/ru/story/2023/11/1446527',
    'https://news.un.org/ru/story/2023/11/1446517',
    'https://news.un.org/ru/story/2023/11/1446497',
    'https://news.un.org/ru/story/2024/02/1449572',
    'https://news.un.org/ru/story/2024/02/1449522',
    'https://news.un.org/ru/story/2024/02/1449492',
    'https://news.un.org/ru/story/2024/02/1449452',
    'https://news.un.org/ru/story/2024/02/1449417',
    'https://news.un.org/ru/story/2024/02/1449382',
    'https://news.un.org/ru/story/2024/02/1449292',
    'https://news.un.org/ru/story/2024/02/1449287',
    'https://news.un.org/ru/story/2024/02/1449272',
    'https://news.un.org/ru/story/2024/02/1449242',
    'https://news.un.org/ru/story/2024/02/1449207',
    'https://news.un.org/ru/story/2024/02/1449192',
    'https://news.un.org/ru/story/2024/02/1449152',
    'https://news.un.org/ru/story/2024/02/1449147',
    'https://news.un.org/ru/story/2024/02/1449102',
    'https://news.un.org/ru/story/2024/01/1449087',
    'https://news.un.org/ru/story/2024/01/1449082',
    'https://news.un.org/ru/story/2024/01/1449022',
    'https://news.un.org/ru/story/2024/01/1448707',
    'https://news.un.org/ru/story/2024/01/1448687',
    'https://news.un.org/ru/story/2024/01/1448647',
    'https://news.un.org/ru/story/2024/01/1448617',
    'https://news.un.org/ru/story/2024/01/1448612',
    'https://news.un.org/ru/story/2024/01/1448607',
    'https://news.un.org/ru/story/2024/01/1448602',
    'https://news.un.org/ru/story/2024/01/1448562',
    'https://news.un.org/ru/story/2024/01/1448487',
    'https://news.un.org/ru/story/2024/01/1448482',
    'https://news.un.org/ru/story/2024/01/1448452',
    'https://news.un.org/ru/story/2024/01/1448437',
    'https://news.un.org/ru/story/2024/01/1448417',
    'https://news.un.org/ru/story/2024/01/1448402',
    'https://news.un.org/ru/story/2024/01/1448367',
    'https://news.un.org/ru/story/2024/01/1448352',
    'https://news.un.org/ru/story/2024/01/1448322',
    'https://news.un.org/ru/story/2023/12/1448192',
    'https://news.un.org/ru/story/2023/12/1448157',
    'https://news.un.org/ru/story/2023/12/1448107',
    'https://news.un.org/ru/story/2023/12/1448087',
    'https://news.un.org/ru/story/2023/12/1448042',
    'https://news.un.org/ru/story/2023/12/1448027',
    'https://news.un.org/ru/story/2023/12/1447997',
    'https://news.un.org/ru/story/2023/12/1447957',
    'https://news.un.org/ru/story/2023/12/1447912',
    'https://news.un.org/ru/story/2023/12/1447877',
    'https://news.un.org/ru/story/2023/12/1447807',
    'https://news.un.org/ru/story/2023/12/1447792',
    'https://news.un.org/ru/story/2023/12/1447767',
    'https://news.un.org/ru/story/2023/12/1447647',
    'https://news.un.org/ru/story/2023/12/1447597',
    'https://news.un.org/ru/story/2023/12/1447552',
    'https://news.un.org/ru/story/2023/12/1447512',
    'https://news.un.org/ru/story/2023/12/1447482',
    'https://news.un.org/ru/story/2023/12/1447397',
    'https://news.un.org/ru/story/2023/12/1447377',
    'https://news.un.org/ru/story/2023/12/1447337',
    'https://news.un.org/ru/story/2023/12/1447322',
    'https://news.un.org/ru/story/2023/11/1447237',
    'https://news.un.org/ru/story/2023/11/1447202',
    'https://news.un.org/ru/story/2023/11/1447142',
    'https://news.un.org/ru/story/2023/11/1447137',
    'https://news.un.org/ru/story/2023/11/1447102',
    'https://news.un.org/ru/story/2023/11/1447087',
    'https://news.un.org/ru/story/2023/11/1447082',
    'https://news.un.org/ru/story/2023/11/1447047',
    'https://news.un.org/ru/story/2023/11/1446987',
    'https://news.un.org/ru/story/2023/11/1446977',
    'https://news.un.org/ru/story/2023/11/1446872',
    'https://news.un.org/ru/story/2023/11/1446837',
    'https://news.un.org/ru/story/2023/11/1446827',
    'https://news.un.org/ru/story/2023/11/1446812',
    'https://news.un.org/ru/story/2023/11/1446807',
    'https://news.un.org/ru/story/2023/11/1446727',
    'https://news.un.org/ru/story/2023/11/1446712',
    'https://news.un.org/ru/story/2023/11/1446687',
    'https://news.un.org/ru/story/2023/11/1446682',
    'https://news.un.org/ru/story/2023/11/1446632',
    'https://news.un.org/ru/story/2023/11/144658',
    'https://news.un.org/ru/story/2023/11/1446587',
    'https://news.un.org/ru/story/2023/11/1446572',
    'https://news.un.org/ru/story/2023/11/1446552',
    'https://news.un.org/ru/story/2023/11/1446542',
    'https://news.un.org/ru/story/2023/11/1446537',
    'https://news.un.org/ru/story/2023/11/1446532',
    'https://news.un.org/ru/story/2023/11/1446442',
    'https://news.un.org/ru/story/2023/10/1446367',
    'https://news.un.org/ru/story/2023/10/1446342',
    'https://news.un.org/ru/story/2023/10/1446337',
    'https://news.un.org/ru/story/2023/10/1446317'
]


def zip_directory(directory, zip_name):
    with zipfile.ZipFile(zip_name, 'w') as zipf:
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, arcname=os.path.relpath(file_path, directory))


def clean_html(html_text):
    # Очищаем от скриптов, ссылок на фотографии
    soup = BeautifulSoup(html_text, 'html.parser')

    for script in soup(["script", "link", "source"]):
        script.extract()
    for img in soup.find_all('img'):
        img.extract()
    for img_link in soup.find_all('a', href=re.compile(r'\.(jpg|png|gif)$')):
        img_link.extract()
    return soup.prettify()


def main():
    directory = 'pages'
    zip_file_name = f'{directory}.zip'
    index_file = open('index.txt', 'w', encoding='utf-8')
    if not os.path.exists(directory):
        os.makedirs(directory)

    file_counter = 1
    for url in urls:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                filename = f'{directory}/{file_counter}.html'
                html_page = clean_html(response.text)

                with open(filename, 'w', encoding='utf-8') as file:
                    file.write(html_page)

                index_file.write(f'{file_counter} {url}\n')
                file_counter += 1
                print(f'{url} downloaded and saved in {filename}')
            else:
                print(f'Error when downloading {url}: status code = {response.status_code}')
        except requests.RequestException as e:
            print(f'Error when downloading {url}: {e}')

    index_file.close()

    zip_directory(directory, zip_file_name)


if __name__ == "__main__":
    main()
