import json

from querying import query
from compare import calculate_metric_for_each


# mock
def prepare_object(params):
    with open('data/tmp.json', 'r') as file:
        return json.load(file)


def metrics_for_query(query_params):
    results = query()
    prepared = prepare_object(query_params)
    return calculate_metric_for_each(prepared, results)


def save_metrics_for_query(scores):
    file_hash = str(hash(str(scores)))
    with open('cache/' + file_hash + '.json', 'w') as file:
        json.dump(scores, file, indent=4)
    return file_hash


def load_metrics_for_query(file_hash):
    with open('cache/' + file_hash + '.json') as file:
        scores = json.load(file)
        return scores
