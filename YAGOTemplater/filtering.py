import rdflib

similar_to = rdflib.URIRef('http://templater.yago.spd.mini.pw.edu.pl/similar_to')
lower_bound = rdflib.URIRef('http://templater.yago.spd.mini.pw.edu.pl/lower_bound')
upper_bound = rdflib.URIRef('http://templater.yago.spd.mini.pw.edu.pl/upper_bound')
equal_to = rdflib.URIRef('http://templater.yago.spd.mini.pw.edu.pl/equal_to')

possible_filters = [
    ('http://schema.org/datePublishedFrom', 'http://schema.org/datePublished', lower_bound),
    ('http://schema.org/datePublishedTo', 'http://schema.org/datePublished', upper_bound),
    ('http://schema.org/composer', 'http://schema.org/composer', equal_to),
    ('http://schema.org/isPartOf', 'http://schema.org/isPartOf', equal_to),
    ('http://schema.org/genre', 'http://schema.org/genre', equal_to),
    ('http://schema.org/inLanguage', 'http://schema.org/inLanguage', equal_to),
    ('http://schema.org/author', 'http://schema.org/author', equal_to)
]
