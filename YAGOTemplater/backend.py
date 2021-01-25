import json
import os

import rdflib

from YAGOTemplater.querying import query
from YAGOTemplater.scoring import calculate_score_for_all
from YAGOTemplater.filtering import *

rdflib.plugin.register('nt', rdflib.plugin.ResultParser, 'rdflib.plugins.parsers.nt', 'NTParser')
rdflib.plugin.register('nt', rdflib.plugin.ResultSerializer, 'rdflib.plugins.serializers.nt', 'NTSerializer')


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


def save_results(query_results):
    query_results.serialize(destination='downloads/results.nt', format='nt')


def store_template_for_download(form_params):
    g = rdflib.Graph()
    for prop in form_params['props'].keys():
        g.add((rdflib.URIRef(prop), similar_to, form_params['props'][prop]))
    for (key, prop, filter_prop) in possible_filters:
        if key in form_params['filters'].keys():
            g.add((rdflib.URIRef(prop), filter_prop, rdflib.Literal(form_params['filters'][key])))
    g.serialize(destination='downloads/template.nt', format='nt')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() == 'nt'


def upload_template(file):
    print(os.getcwd())
    if file and allowed_file(file.filename):
        file.save(os.path.join(os.getcwd(), 'uploads', 'template.nt'))


def read_template():
    if os.path.exists('uploads/template.nt'):
        g = rdflib.Graph()
        g.parse('uploads/template.nt', format='nt')
        os.remove('uploads/template.nt')
        return parse_template(g)
    else:
        return {}


def parse_template(graph):
    ret = {}
    for (s, p, o) in graph:
        if p == rdflib.term.URIRef('http://templater.yago.spd.mini.pw.edu.pl/equal_to'):
            ret['filters-' + str(s)] = str(o)
        elif p == rdflib.term.URIRef('http://templater.yago.spd.mini.pw.edu.pl/lower_bound'):
            ret['filters-' + str(s) + "From"] = str(o)
        elif p == rdflib.term.URIRef('http://templater.yago.spd.mini.pw.edu.pl/upper_bound'):
            ret['filters-' + str(s) + "To"] = str(o)
        if p == rdflib.term.URIRef('http://templater.yago.spd.mini.pw.edu.pl/similar_to'):
            ret['param-' + str(s)] = str(o)
    return ret
