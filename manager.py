__author__ = 'vladimirsusaya'
from scraper import run_scraper
from media_scraper import run_media_scraper
import pprint
import json

    
pp = pprint.PrettyPrinter(indent=4)
url = 'http://tvtropes.org/pmwiki/pmwiki.php/Main/SignificantGreenEyedRedhead'

corpus = {}
queue = [ ['t', url] ]  #queue of urls to examine

ext_count = 0
for i in range(1000):
	ext_count += 1
	url = queue.pop(0)

	#try:
	if url[0] == 't':
		#insert scraper data into the corpus
		page_data = run_scraper(url[1])

		if page_data is None:
			continue

		corpus[str(i)] = page_data
		#print page_data

		try:
			#get the links and put them into the queue
			links = page_data[unicode('Literature', "utf-8")]
			for key in links:
				queue.append(['m', links[key]])
				break
		except:
			continue

	else:
		#insert scraper data into the corpus
		page_data = run_media_scraper(url[1])

		if page_data is None:
			continue

		corpus[str(i)] = page_data

		#get the links and put them into the queue
		try:
			links = page_data[unicode('tropes', "utf-8")]
			for key in links:
				queue.append(['t', links[key]])
		except:
			continue

	#except:
		#continue


json_data = json.dumps(corpus)
f = open('corpus.json', 'w')
f.write(json_data)

print ext_count
print len(corpus.keys())
#pp.pprint(corpus)
#pp.pprint(page_data)