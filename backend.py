import json

from querying import mock_query
from scoring import calculate_score_for_all


# mock
def prepare_object(params):
    with open('data/tmp.json', 'r') as file:
        return json.load(file)


def scores_for_query(query_params):
    results = mock_query()
    prepared = prepare_object(query_params)
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
