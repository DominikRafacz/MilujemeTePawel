import dateutil.parser as parser
from rdflib import Namespace
from rdflib.namespace import FOAF, RDF, RDFS, XSD
from rdflib.plugins.stores.sparqlstore import SPARQLStore
from util import EmptyFormException


def check_form_params(form_params):
    if all(map(lambda key: (form_params['props'][key] == ''), form_params['props'].keys())):
        raise EmptyFormException('Form has no field filled')


# mock
def prepare_filter_string(form_params):
    return ''


def get_chosen_properties_filter():
    return """
    FILTER(?prop IN (<http://www.w3.org/2000/01/rdf-schema#label>, <http://www.w3.org/2000/01/rdf-schema#comment>, 
        schema:alternateName, schema:datePublished, schema:composer, schema:isPartOf, schema:genre, schema:inLanguage, 
        schema:lyricist, schema:producer, schema:dateCreated, schema:author, schema:isBasedOn, schema:about, schema:award, 
        schema:creator, schema:contributor, schema:publisher, schema:translator)) 
    """


def prepare_queery(form_params):
    query_string = """
            SELECT ?item ?prop ?val
            WHERE {
                ?item rdf:type schema:MusicComposition ;
                    ?prop ?val .""" + \
                   get_chosen_properties_filter() + \
                   prepare_filter_string(form_params) + \
                   """
           }
           LIMIT 10000
           """
    return query_string


def get_namespaces():
    schema = Namespace("http://schema.org/")
    ns = dict(rdf=RDF, foaf=FOAF, rdfs=RDFS, xsd=XSD, schema=schema)
    return ns


# ex params: {'props' : {'http://www.w3.org/2000/01/rdf-schema#label' : 'pioseneczka', 'http://schema.org/dateCreated': '2010'}}

def query(form_params):
    namespaces = get_namespaces()
    sparql_store = SPARQLStore("https://yago-knowledge.org/sparql/query")
    query_string = prepare_queery(form_params)
    result = sparql_store.query(query_string, initNs=namespaces)
    # for row in list(result):
    #     print(row)
    return reformat_results(result)


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

