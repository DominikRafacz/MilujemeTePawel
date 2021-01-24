from setuptools import setup

setup(
    name='YAGO Search Song By Template',
    version='0.1',
    long_description=__doc__,
    packages=['YAGOTemplater'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
    entry_points={
        'rdf.plugins.parser': [
            'nt =     rdf.plugins.parsers.nt:NTParser',
        ],
        'rdf.plugins.serializer': [
            'nt =     rdf.plugins.serializers.NTSerializer:NTSerializer',
        ],
    }
)
