from SPARQLWrapper import SPARQLWrapper, JSON
import json
import dateutil.parser as parser

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
results = sparql.query().convert()


prop = {}
for result in results["results"]["bindings"]:
    # try:
    #     prop[result['prop']['value']]
    # except (KeyError) as e:
    #     prop[result['prop']['value']] = set()

    prop[result['prop']['value']] = result['val']['type']

print(json.dumps(prop, indent=4))


