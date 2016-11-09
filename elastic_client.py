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

def health_check():
    es = Elasticsearch([{'host': 'local.docker.dev'}])
    print es.info()

def reset_index():
    es = Elasticsearch([{'host': 'local.docker.dev'}])
    print es.indices.delete("scrapy")
    print es.indices.create(index='scrapy', ignore=400)


def delete_index():
    es = Elasticsearch([{'host': 'local.docker.dev'}])
    print es.indices.delete("scrapy")


def create_index():
    es = Elasticsearch([{'host': 'local.docker.dev'}])
    print es.indices.create(index='scrapy', ignore=400)