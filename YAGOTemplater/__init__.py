from flask import Flask, render_template, request, redirect, url_for, send_file

from YAGOTemplater.querying import check_form_params, reformat_results
from YAGOTemplater.util import load_chosen_properties, EmptyFormException
from YAGOTemplater.backend import *
from rdflib.term import URIRef, Literal

app = Flask(__name__)

fields = load_chosen_properties()


@app.route('/')
def index():
    return redirect(url_for('form'))


@app.route('/form', methods=('GET', 'POST'))
def form():
    if request.method == 'POST':
        form_params = {'props': {field: URIRef(request.form['param-' + field]) if request.form['param-' + field][:7] == 'http://' else Literal(request.form['param-' + field]) for field in fields if request.form['param-' + field] != ''},
                       'filters': {field: request.form['filters-' + field] for field in fields if 'filters-' + field in request.form.keys() and request.form['filters-' + field] != ''}}
        try:
            check_form_params(form_params)
        except EmptyFormException:
            return redirect('invalid_form')
        query_results = query(form_params)
        save_results(query_results)
        query_results = reformat_results(query_results)
        prepared = prepare_object(form_params)
        scores = calculate_score_for_all(prepared, query_results)
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


@app.route('/download')
def download():
    return send_file("../downloads/results.nt", as_attachment=True)


if __name__ == '__main__':
    app.run()
