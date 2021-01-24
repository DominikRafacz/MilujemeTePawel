import json
import os


def load_chosen_properties():
    print(os.getcwd())
    with open('YAGOTemplater/data/chosen_properties.json') as file:
        chosen = json.load(file)
        return list(chosen.keys())


class EmptyFormException(Exception):
    pass
