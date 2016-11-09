import argparse

import elastic_client
from crawler_starter import launch_crawlers


parser = argparse.ArgumentParser(description='Zero scraper!')

parser.add_argument('--action', '-a',
                    help='choose your action',
                    choices=['create', 'delete', 'reset', 'crawl', 'health-check'],
                    required=True)

parser.add_argument('target',
                    nargs='?',
                    help='what do you want to crawl? (all|spider)')

args = parser.parse_args()


def crawl():
    launch_crawlers(args.target)

actions = {
    "create": elastic_client.create_index,
    "delete": elastic_client.delete_index,
    "reset": elastic_client.reset_index,
    "crawl": crawl,
    "health-check": elastic_client.health_check
}

if args.action:
    actions[args.action]()
