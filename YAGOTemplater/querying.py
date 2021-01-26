import dateutil.parser as parser
from rdflib import Namespace
from rdflib.namespace import FOAF, RDF, RDFS, XSD
from rdflib.plugins.stores.sparqlstore import SPARQLStore
from YAGOTemplater.util import EmptyFormException
import json


def check_form_params(form_params):
    if all(map(lambda key: (form_params['props'][key] == ''), form_params['props'].keys())):
        raise EmptyFormException('Form has no field filled')


# mock
def prepare_filter_string(form_params):
    parms_getters = {
        "http://schema.org/datePublishedFrom": "?item <http://schema.org/datePublished> ?date .",
        "http://schema.org/datePublishedTo": "?item <http://schema.org/datePublished> ?date .",
        "http://schema.org/composer": "?item <http://schema.org/composer> ?composer .",
        "http://schema.org/isPartOf": "?item <http://schema.org/isPartOf> ?isPartOf .",
        "http://schema.org/genre": "?item <http://schema.org/genre> ?genre .",
        "http://schema.org/inLanguage": "?item <http://schema.org/inLanguage> ?inLanguage .",
        "http://schema.org/author": "?item <http://schema.org/author> ?author ."
    }
    upper = ''
    lower = ''
    for key in list(form_params.keys()):
        upper += parms_getters[key] + "\n"
        if key == "http://schema.org/datePublishedFrom":
            if form_params["http://schema.org/datePublishedFrom"] is not None:
                lower += "FILTER(year(strdt(str(?date), xsd:date )) >= year(\"" + form_params["http://schema.org/datePublishedFrom"] \
                         + "\"^^xsd:date)) .\n"
        elif key == "http://schema.org/datePublishedTo":
            if form_params["http://schema.org/datePublishedTo"] is not None:
                lower += "FILTER(year(strdt(str(?date), xsd:date )) <= year(\"" + form_params["http://schema.org/datePublishedTo"] \
                         + "\"^^xsd:date)) .\n"
        elif key == "http://schema.org/composer":
            lower += "FILTER(?composer = <" + form_params["http://schema.org/composer"] + ">) .\n"
        elif key == "http://schema.org/isPartOf":
            lower += "FILTER(?isPartOf = <" + form_params["http://schema.org/isPartOf"] + ">) .\n"
        elif key == "http://schema.org/genre":
            lower += "FILTER(?genre = <" + form_params["http://schema.org/genre"] + ">) .\n"
        elif key == "http://schema.org/inLanguage":
            lower += "FILTER(?inLanguage = <" + form_params["http://schema.org/inLanguage"] + ">) .\n"
        elif key == "http://schema.org/author":
            lower += "FILTER(?author = <" + form_params["http://schema.org/author"] + ">) .\n"

    return upper + lower


def get_chosen_properties_filter():
    return """
    FILTER(?prop IN (<http://www.w3.org/2000/01/rdf-schema#label>, <http://www.w3.org/2000/01/rdf-schema#comment>, 
        schema:alternateName, schema:datePublished, schema:composer, schema:isPartOf, schema:genre, schema:inLanguage, 
        schema:lyricist, schema:producer, schema:dateCreated, schema:author, schema:isBasedOn, schema:about, schema:award, 
        schema:creator, schema:contributor, schema:publisher, schema:translator)) 
    """


def prepare_query(form_params):
    query_string = """
            SELECT ?item ?prop ?val
            WHERE {
                ?item rdf:type schema:MusicComposition ;
                    ?prop ?val .""" + \
                   get_chosen_properties_filter() + \
                   prepare_filter_string(form_params['filters']) + \
                   """
           }
           """
    print(json.dumps(form_params, indent=4))
    print(query_string)
    return query_string


def get_namespaces():
    schema = Namespace("http://schema.org/")
    ns = dict(rdf=RDF, foaf=FOAF, rdfs=RDFS, xsd=XSD, schema=schema)
    return ns


# ex params: {'props' : {'http://www.w3.org/2000/01/rdf-schema#label' : 'pioseneczka', 'http://schema.org/dateCreated': '2010'}}

def query(form_params):
    namespaces = get_namespaces()
    sparql_store = SPARQLStore("https://yago-knowledge.org/sparql/query")
    query_string = prepare_query(form_params)
    result = sparql_store.query(query_string, initNs=namespaces)
    # for row in list(result):
    #     print(row)
    return result


# returns dict: '<entity_uri>' : [{'prop' : '<property_uri>', 'val': } ...]
def reformat_results(results):
    ret = {}
    for result in list(results):
        try:
            ret[str(result[0])]
        except KeyError:
            ret[str(result[0])] = []

        if str(result[1]) in ("http://schema.org/dateCreated", "http://schema.org/datePublished"):
            val = parser.parse(str(result[2])).year
        else:
            val = result[2]
        # print(val)
        ret[str(result[0])].append({"prop": str(result[1]), "val": val})
    return ret

