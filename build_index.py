__author__ = 'Tiffany Chen'

from elasticsearch import Elasticsearch, helpers
import sys
import json

es = Elasticsearch()

json_data = open('mapping.json').read()
body = json.dumps(json.loads(json_data))

ts_index = es.indices.create(index = "tropes_and_media", body = body)

##do bulk loading
def format_action(id, value):
	return {
		"_index": "tropes_and_media",
		"_type": "item",
		"_id": int(id),
		"_source": value
	}

items = json.load(open('corpus.json'))

actions = []
for key, value in items.iteritems():
	actions.append(format_action(key, value))

helpers.bulk(es, actions, stats_only = True)

es.indices.refresh(index='tropes_and_media')
#print(es.count(index='tropes_and_media'))
#print(es.indices.get_mapping("tropes_and_media"))

#es.indices.delete(index = "tropes_and_media")