from SPARQLWrapper import SPARQLWrapper, JSON
import dateutil.parser as parser
from rdflib.plugins.stores.sparqlstore import SPARQLStore
from rdflib import Namespace
from rdflib.namespace import FOAF, RDF, RDFS, XSD
from rdflib.term import Literal, URIRef


def reformat_results(results):
    ret = {}
    for result in results["results"]["bindings"]:
        try:
            ret[result['item']['value']]
        except KeyError:
            ret[result['item']['value']] = []

        if result['prop']['value'] in ("http://schema.org/dateCreated", "http://schema.org/datePublished"):
            result['val']['value'] = parser.parse(result['val']['value']).year
        ret[result['item']['value']].append({"prop": result['prop'], "val": result['val']})
    return ret


# mock function
def mock_query():
    sparql = SPARQLWrapper("https://yago-knowledge.org/sparql/query")
    sparql.setQuery("""
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX schema: <http://schema.org/>
        SELECT ?item ?prop ?val
        WHERE
        {
        ?item rdf:type schema:MusicComposition ;
            ?prop ?val . 
        FILTER(?prop IN (<http://www.w3.org/2000/01/rdf-schema#label>, <http://www.w3.org/2000/01/rdf-schema#comment>, 
        schema:alternateName, schema:datePublished, schema:composer, schema:isPartOf, schema:genre, schema:inLanguage, 
        schema:lyricist, schema:producer, schema:dateCreated, schema:author, schema:isBasedOn, schema:about, schema:award, 
        schema:creator, schema:contributor, schema:publisher, schema:translator)
    )
        }
    LIMIT 1000
    """)
    sparql.setReturnFormat(JSON)
    return reformat_results(sparql.query().convert())


def get_namespaces():
    schema = Namespace("http://schema.org/")
    ns = dict(rdf=RDF, foaf=FOAF, rdfs=RDFS, xsd=XSD, schema=schema)
    return ns


def rdf_query():

    namespaces = get_namespaces()
    sparql_store = SPARQLStore("https://yago-knowledge.org/sparql/query")

    query_string = """
    SELECT ?item ?prop ?val
    WHERE
    {
        ?item rdf:type schema:MusicComposition ;
              ?prop ?val . 
        FILTER(?prop IN (<http://www.w3.org/2000/01/rdf-schema#label>, <http://www.w3.org/2000/01/rdf-schema#comment>, 
        schema:alternateName, schema:datePublished, schema:composer, schema:isPartOf, schema:genre, schema:inLanguage, 
        schema:lyricist, schema:producer, schema:dateCreated, schema:author, schema:isBasedOn, schema:about, 
        schema:award, schema:creator, schema:contributor, schema:publisher, schema:translator))
    }
    LIMIT 1000
    """

    result = sparql_store.query(query_string, initNs=namespaces)
    # for row in list(result):
    #     print(row)
    return result


def reformat_results_rdf(results):
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
        print(val)
        ret[str(result[0])].append({"prop": str(result[1]), "val": val})
    return ret


results = rdf_query()
response = reformat_results_rdf(results)
