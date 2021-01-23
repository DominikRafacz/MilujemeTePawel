from flask import Flask, render_template, request, redirect, url_for
from util import load_chosen_properties
from backend import *

app = Flask(__name__)

fields = load_chosen_properties()


@app.route('/')
def index():
    return redirect(url_for('form'))


@app.route('/form', methods=('GET', 'POST'))
def form():
    if request.method == 'POST':
        query_params = {field: request.form[field] for field in fields}
        scores = scores_for_query(query_params)
        scores_hash = save_scores(scores)
        return redirect(url_for('results', scores_hash=scores_hash))
    return render_template('form.html.jinja2', fields=fields)


@app.route('/results/<scores_hash>')
def results(scores_hash):
    scores = load_scores(scores_hash)
    return render_template('results.html.jinja2', scores=scores)


if __name__ == '__main__':
    app.run()
