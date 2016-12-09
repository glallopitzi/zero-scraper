import json

from elasticsearch import Elasticsearch

CONFIG_FOLDER = "config/"

# # print es.indices.exists(index='scrapy')
# # print es.count(index='scrapy')
# already_seen_url = []
# res = es.search(index='scrapy', filter_path=['hits.hits._source.url'], q='website:subito.it', size=1000)
# for elem in res['hits']['hits']:
#     already_seen_url.append(elem['_source']['url'])
#
# # res_string = json.dumps(res)
# # res_obj = json.loads(res_string)
# # print res_obj['hits']
# # for url in res_obj['hits']['hits']:
# #     print url
# # print json.dumps(es.indices.analyze(index='scrapy'))

es = Elasticsearch([{'host': 'local.docker.dev'}])


def count_element():
    print es.count(index="scrapy")

def health_check():
    print es.info()


def reset_index():
    count_element()
    delete_index()
    create_index()
    count_element()


def delete_index():
    print es.indices.delete("scrapy")


def create_index():
    with open(CONFIG_FOLDER + 'index.json') as data_file:
        settings = json.load(data_file)

    print es.indices.create(index='scrapy', body=settings, ignore=400)
