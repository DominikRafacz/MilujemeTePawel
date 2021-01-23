from SPARQLWrapper import SPARQLWrapper, JSON
import dateutil.parser as parser


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


# mock function
def query():
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
