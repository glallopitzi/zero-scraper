import argparse
import crawler_starter
import elastic_client


parser = argparse.ArgumentParser(description='Zero scraper!')

parser.add_argument('--action', '-a',
                    help='choose your action',
                    choices=['create', 'delete', 'reset', 'search', 'health-check', 'crawl'],
                    required=True)

parser.add_argument('--category', '-c',
                    help='choose your category',
                    choices=['home', 'motor', 'generic'],
                    required=True)

parser.add_argument('target',
                    nargs='?',
                    help='what do you want to crawl? (all|spider)')

args = parser.parse_args()


actions = {
    "create": elastic_client.create_index,
    "delete": elastic_client.delete_index,
    "reset": elastic_client.reset_index,
    "health-check": elastic_client.health_check,
    "search": elastic_client.search,
    "crawl": crawler_starter.launch_crawlers
}

if args.action:
    if args.target:
        actions[args.action](args.target)
    else:
        actions[args.action]()

