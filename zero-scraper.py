import argparse

import elastic_client
from crawler_starter import launch_crawlers

parser = argparse.ArgumentParser(description='Zero scraper!')

parser.add_argument('--action', '-a',
                    help='choose your action',
                    choices=['create', 'delete', 'reset', 'crawl', 'health-check'],
                    required=True)

args = parser.parse_args()


actions = {
    "create": elastic_client.create_index,
    "delete": elastic_client.delete_index,
    "reset": elastic_client.reset_index,
    "crawl": launch_crawlers,
    "health-check": elastic_client.health_check
}

if args.action:
    actions[args.action]()
