import config_loader

from elasticsearch import Elasticsearch

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

es = Elasticsearch([{'host': 'localhost'}])


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
    mappings = config_loader.load_json_from_file('index')
    print es.indices.create(index='scrapy', body=mappings, ignore=400)
