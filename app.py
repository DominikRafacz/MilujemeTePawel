from flask import Flask, render_template, request, redirect, url_for

from querying import check_form_params
from util import load_chosen_properties, EmptyFormException
from backend import *

app = Flask(__name__)

fields = load_chosen_properties()


@app.route('/')
def index():
    return redirect(url_for('form'))


@app.route('/form', methods=('GET', 'POST'))
def form():
    if request.method == 'POST':
        form_params = {'props': {field: request.form[field] for field in fields}}
        try:
            check_form_params(form_params)
        except EmptyFormException:
            return redirect('invalid_form')
        scores = scores_for_query(form_params)
        scores_hash = save_scores(scores)
        return redirect(url_for('results', scores_hash=scores_hash))
    return render_template('form.html.jinja2', fields=fields)


@app.route('/results/<scores_hash>')
def results(scores_hash):
    scores = load_scores(scores_hash)
    return render_template('results.html.jinja2', scores=scores)


@app.route('/invalid_form')
def invalid_form():
    return render_template('invalid_form.html')


if __name__ == '__main__':
    app.run()
