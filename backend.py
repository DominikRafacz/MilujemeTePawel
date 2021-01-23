import json

import rdflib
from rdflib.term import Literal

from querying import query
from scoring import calculate_score_for_all


def prepare_object(params):
    return [{'prop': prop, 'val': rdflib.term.Literal(params['props'][prop])}
            for prop in params['props'].keys() if params['props'][prop] != '']


def scores_for_query(form_params):
    results = query(form_params)
    prepared = prepare_object(form_params)
    return calculate_score_for_all(prepared, results)


def save_scores(scores):
    file_hash = str(hash(str(scores)))
    with open('cache/' + file_hash + '.json', 'w') as file:
        json.dump(scores, file, indent=4)
    return file_hash


def load_scores(file_hash):
    with open('cache/' + file_hash + '.json') as file:
        scores = json.load(file)
        return scores
