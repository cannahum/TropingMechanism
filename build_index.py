__author__ = 'Tiffany Chen'

from elasticsearch import Elasticsearch, helpers
import sys
import json

es = Elasticsearch()

json_data = open('mapping.json').read()
body = json.dumps(json.loads(json_data))

##do bulk loading
def format_action(id, value):
	return {
		"_index": "tropes_and_media",
		"_type": "item",
		"_id": int(id),
		"_source": value
	}

def buildindex():
    ts_index = es.indices.create(index = "tropes_and_media", body = body)
    '''items = json.load(open('corpus.json'))'''
    items = json.load(open('corpus_test.json'))
    '''items = json.load(open('corpus_0.json'))'''

    actions = []
    for key, value in items.iteritems():
	    actions.append(format_action(key, value))
    helpers.bulk(es, actions, stats_only = True, request_timeout=60)
    es.indices.refresh(index='tropes_and_media')

##QUERY METHODS
def exsearch(query):
    res = es.search(index='tropes_and_media', doc_type='item', body={"query": {
    "filtered": {
       "query": {"match_all": {}},
       "filter": {
          "and": [
            {"term": {"links.genre": query}},
            {"term": {"links.titleofwork":"Justice League"}}
          ]
       }
    }
  }
})
    #{'bool':{'should':[{'multi_match':{'query':query,'fields':['links.genre']}}]}}})
    lst = []
    print res['hits']['hits']

##buildindex()
u = unicode('Comic Books', "utf-8")
exsearch(u)
#print(es.count(index='tropes_and_media'))
#print(es.indices.get_mapping("tropes_and_media"))

# for deleting indices, but can also do it in terminal
#es.indices.delete(index = "tropes_and_media")