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
        ?prop ?val . }
    LIMIT 100
""")
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

# print(json.dumps(results["results"]["bindings"], indent=4))


print(len(results["results"]["bindings"]))

tmp = {}
for result in results["results"]["bindings"]:
    try:
        tmp[result['item']['value']]
    except (KeyError) as e:
        tmp[result['item']['value']] = []

    tmp[result['item']['value']].append({"prop":result['prop'], "val": result['val']})

print(json.dumps(tmp, indent=4))
