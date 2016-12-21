import json

CONFIG_FOLDER = "config/"

ITEMS_TYPE = "generic" # home or generic or motor


def load_json_from_file(file):
    with open(CONFIG_FOLDER + ITEMS_TYPE + '/' + file + '.json') as data_file:
        return json.load(data_file)
