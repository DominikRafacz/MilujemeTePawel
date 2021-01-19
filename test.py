from SPARQLWrapper import SPARQLWrapper, JSON
import json

sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
sparql.setQuery("""
    SELECT ?item ?prop ?val
    WHERE 
    {
    ?item wdt:P31 wd:Q7366;
       ?prop ?val . }
    LIMIT 100
""")
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

print(len(results["results"]["bindings"]))

tmp = {}
for result in results["results"]["bindings"]:
    try:
        tmp[result['item']['value']]
    except (KeyError) as e:
        tmp[result['item']['value']] = []
        
    tmp[result['item']['value']].append({"prop":result['prop'], "val": result['val']})

print(json.dumps(tmp, indent=4))