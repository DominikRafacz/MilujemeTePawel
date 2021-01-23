import json


def load_chosen_properties():
    with open('data/chosen_properties.json') as file:
        chosen = json.load(file)
        return list(chosen.keys())


class EmptyFormException(Exception):
    pass
