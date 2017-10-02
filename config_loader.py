import json
from ConfigParser import RawConfigParser

from jsonmerge import merge

CONFIG_FOLDER = "config/"
COMMON_FOLDER = "common/"

ES_FOLDER = "es/"
SCRAPER_FOLDER = "scraper/"
PORTAL_FOLDER = "portal/"

ITEMS_TYPE = "home" # home or generic or motor
# or 'generic' or 'motor'

settings_lookup_table = {
    "index": ES_FOLDER,
    "settings": SCRAPER_FOLDER,
    "pipeline": SCRAPER_FOLDER,
    "crawlers": SCRAPER_FOLDER,
    "search_body": ES_FOLDER
}

def set_items_type(category):
    ITEMS_TYPE = category


def get_items_type():
    return ITEMS_TYPE


def get_items_type_folder():
    return get_items_type() + '/'


def load_json_from_file(file):
    with open(CONFIG_FOLDER + ITEMS_TYPE + '/' + file + '.json') as data_file:
        return json.load(data_file)


def load_config(name):
    parser = RawConfigParser()

    common_portal = CONFIG_FOLDER + COMMON_FOLDER + PORTAL_FOLDER + name + ".cfg"
    specific_portal = CONFIG_FOLDER + ITEMS_TYPE + "/" + PORTAL_FOLDER + name + ".cfg"

    parser.readfp(open(common_portal))
    parser.read(specific_portal)
    return parser


def load_json_from_file(settings_file_to_load):

    settings_subfolder = settings_lookup_table[settings_file_to_load]
    if settings_subfolder is None:
        settings_subfolder = PORTAL_FOLDER

    with open(CONFIG_FOLDER + COMMON_FOLDER + settings_subfolder + settings_file_to_load + '.json') as data_file:
        common = json.load(data_file)

    with open(CONFIG_FOLDER + get_items_type_folder() + settings_subfolder + settings_file_to_load + '.json') as data_file:
        specific = json.load(data_file)

    result = merge(common, specific)
    return result
