import json
from flask import Flask, render_template, url_for, request
import requests


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def main_page():
    results = []
    term = ''

    if request.method == 'POST' and 'term' in request.form:
        term = request.form['term']
        url = 'http://demo.ckan.org/api/action/datastore_search?resource_id=4f30b925-0d6a-4864-865c-e018b57bd558&q='+term
        response = requests.get(url)
        data = json.loads(response.content)
        results = data["result"]["records"]

    return render_template('index.html', results=results, term=term)

@app.route('/maptest')
def map_test():
    return render_template('maptest.html')

if __name__ == '__main__':
    app.run()
