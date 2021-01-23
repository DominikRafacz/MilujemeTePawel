from flask import Flask, render_template, request, redirect, url_for
from util import load_chosen_properties

app = Flask(__name__)

fields = load_chosen_properties()


def metrics_for_query(query_params):
    return {'some_result': None}


@app.route('/')
def index():
    return redirect(url_for('form'))


@app.route('/form', methods=('GET', 'POST'))
def form():
    if request.method == 'POST':
        query_params = {field: request.form[field] for field in fields}
        metrics_results = metrics_for_query(query_params)
        return redirect(url_for('results', metrics_results=metrics_results))
    return render_template('form.html.jinja2', fields=fields)


@app.route('/results/<metrics_results>')
def results(metrics_results):
    return render_template('results.html.jinja2', metrics_results=metrics_results)


if __name__ == '__main__':
    app.run()
