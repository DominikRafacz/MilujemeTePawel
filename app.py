from flask import Flask, render_template

app = Flask(__name__)

fields = ['label', 'comment', 'alternateName', 'datePublished', 'composer', 'isPartOf']


@app.route('/form')
def form():
    return render_template('form.html.jinja2', fields=fields)


if __name__ == '__main__':
    app.run()
