import json


def load_chosen_properties():
    with open('chosen_properties.json') as file:
        chosen = json.load(file)
        return list(chosen.keys())
