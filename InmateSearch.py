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
        url = 'http://demo.ckan.org/api/action/datastore_search?resource_id=afeb9507-52cb-484e-a160-338b2326a5c8&q='+term
        response = requests.get(url)
        data = json.loads(response.content)
        results = data["result"]["records"]

    return render_template('index.html', results=results, term=term)


if __name__ == '__main__':
    app.run()
