from flask import Flask, render_template, request, redirect, url_for, send_file

from YAGOTemplater.querying import check_form_params, reformat_results
from YAGOTemplater.util import load_chosen_properties, EmptyFormException, extract_params
from YAGOTemplater.backend import *

app = Flask(__name__)
fields = load_chosen_properties()


@app.route('/')
def index():
    return redirect(url_for('form'))


@app.route('/form/', methods=('GET', 'POST'))
def form():
    if request.method == 'POST':
        if 'file' in request.files:
            upload_template(request.files['file'])
            return redirect(request.url)
        form_params = extract_params(request, fields)
        try:
            check_form_params(form_params)
        except EmptyFormException:
            return redirect('invalid_form')
        if 'option-save' in request.form.keys() and request.form['option-save'] == 'on':
            store_template_for_download(form_params)
            return redirect(url_for('download_template'))
        query_results = query(form_params)
        save_results(query_results)
        query_results = reformat_results(query_results)
        prepared = prepare_object(form_params)
        scores = calculate_score_for_all(prepared, query_results)
        scores_hash = save_scores(scores)
        return redirect(url_for('results', scores_hash=scores_hash))
    template = read_template()
    return render_template('form.html.jinja2', fields=fields, template=template)


@app.route('/results/<scores_hash>')
def results(scores_hash):
    scores = load_scores(scores_hash)
    return render_template('results.html.jinja2', scores=scores)


@app.route('/invalid_form')
def invalid_form():
    return render_template('invalid_form.html')


@app.route('/download_results')
def download_results():
    return send_file("../downloads/results.nt", as_attachment=True)


@app.route('/download_template')
def download_template():
    return send_file("../downloads/template.nt", as_attachment=True)


if __name__ == '__main__':
    app.run()
