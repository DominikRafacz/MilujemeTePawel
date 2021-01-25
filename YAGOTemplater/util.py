import json
import os

from rdflib import URIRef, Literal


def load_chosen_properties():
    print(os.getcwd())
    with open('YAGOTemplater/data/chosen_properties.json') as file:
        chosen = json.load(file)
        return list(chosen.keys())


class EmptyFormException(Exception):
    pass


def extract_params(request, fields):
    return {'props': {
        field: URIRef(request.form['param-' + field])
        if request.form['param-' + field][:7] == 'http://'
        else Literal(request.form['param-' + field])
        for field in fields if request.form['param-' + field] != ''},
            'filters': {
        field[8:]: request.form[field]
        for field in list(request.form.keys())
        if field[:8] == 'filters-' and request.form[field] != ''}}
