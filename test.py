from SPARQLWrapper import SPARQLWrapper, JSON
import json

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


tmp = {}
for result in results["results"]["bindings"]:
    try:
        tmp[result['item']['value']]
    except (KeyError) as e:
        tmp[result['item']['value']] = []

    tmp[result['item']['value']].append({"prop": result['prop'], "val": result['val']})

print(json.dumps(tmp, indent=4))


