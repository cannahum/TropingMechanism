import shelve
import json

my_shelve = shelve.open("shelve_corpus.db")
f = open('corpus.json', 'r')
data = json.load(f)
my_shelve.update(data)