import dateutil.parser as parser
from rdflib.plugins.stores.sparqlstore import SPARQLStore
from rdflib import Namespace
from rdflib.namespace import FOAF, RDF, RDFS, XSD
from rdflib.term import Literal, URIRef


def prepare_queery(query_params):
    print(query_params)
    params = [prop for prop in query_params.keys() if query_params[prop] != '']
    if len(params) == 0:
        raise BaseException
    query_string = """
            SELECT ?item ?prop ?val
            WHERE {
                ?item rdf:type schema:MusicComposition ;
                    ?prop ?val .
                FILTER(?prop IN (<""" + \
                   ">, <".join(params) + \
                   """>))
           }
           LIMIT 1000
           """
    return query_string


def get_namespaces():
    schema = Namespace("http://schema.org/")
    ns = dict(rdf=RDF, foaf=FOAF, rdfs=RDFS, xsd=XSD, schema=schema)
    return ns


#ex params: {'http://www.w3.org/2000/01/rdf-schema#label' : 'pioseneczka', 'http://schema.org/dateCreated': '2010'}

def query(query_params):
    namespaces = get_namespaces()
    sparql_store = SPARQLStore("https://yago-knowledge.org/sparql/query")
    query_string = prepare_queery(query_params)
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
        #print(val)
        ret[str(result[0])].append({"prop": str(result[1]), "val": val})
    return ret


# results = rdf_query()
# response = reformat_results_rdf(results)
