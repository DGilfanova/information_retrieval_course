from flask import Flask, render_template, request
from task_5.main import process_query
 
INDEX_FILE = 'index.txt'
app = Flask(__name__, template_folder='template')


def read_index():
    links = {}
    with open(INDEX_FILE, 'r', encoding='utf-8') as file:
        for line in file.readlines():
          links[line.split(" ")[0]] = line.split(" ")[1].replace("\n","")
    return links


def get_link_results(search_result, links):
    if search_result is not None and search_result:
        responses = []
        for item in search_result:
            responses.append(links[str(item)])
        return responses
    else:
        return None


@app.route('/', methods=['GET', 'POST'])
def index():
    links = read_index()
    if request.method == 'GET':
        return render_template('search.html')
    else:
        input_value = request.form['input_value']
        result = process_query(input_value)
        links_result = get_link_results(result, links)
        if links_result is not None:
            return render_template('result.html', input_value=input_value, result=links_result[:10])
        else:
            return render_template('bad_result.html', input_value=input_value)


if __name__ == '__main__':
    app.run()
