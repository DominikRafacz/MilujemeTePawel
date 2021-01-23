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
        <http://schema.org/image> ?val  }
""")
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

tmp = {}
for result in results["results"]["bindings"]:
    try:
        tmp[result['prop']['value']]
    except (KeyError) as e:
        tmp[result['prop']['value']] = 0

    tmp[result['prop']['value']] += 1

tmp = {k: v for k, v in sorted(tmp.items(), key=lambda item: -item[1])}

print(json.dumps(tmp, indent=4))
