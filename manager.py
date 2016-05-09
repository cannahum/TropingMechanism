__author__ = 'vladimirsusaya'
from trope_scraper import run_trope_scraper
from media_scraper import run_media_scraper
import pprint
import json
import re

    
pp = pprint.PrettyPrinter(indent=4)
url = 'http://tvtropes.org/pmwiki/pmwiki.php/Main/SignificantGreenEyedRedhead'

corpus = {}
queue = [ ['t', url] ]  #queue of urls to examine
mediatypeRE = re.compile

#check for duplicate links
examined_tropes = [url]
examined_media = []

#check which links failed
failed_tropes = []
failed_media = []
exception_ctr_t = 0
exception_ctr_m = 0

ext_count = 0
for i in range(100):
	ext_count += 1
	url = queue.pop(0)

	#try:
	if url[0] == 't':
		#insert scraper data into the corpus
		#scrapers return None value if it fails
		page_data = run_trope_scraper(url[1])

		if page_data is None:
			failed_tropes.append(url[1])
			continue

		corpus[str(i)] = page_data

		try:
			#get the links and put them into the queue
			#don't put anything in the queue that we've seen already
			links = page_data["links"][unicode('Literature', "utf-8")]
			for key in links:
				if links[key] not in examined_media:
					queue.append(['m', links[key]])
					examined_media.append(links[key])
		except:
			exception_ctr_t += 1
			continue

	else:
		#insert scraper data into git the corpus
		page_data = run_media_scraper(url[1])

		if page_data is None:
			failed_media.append(url[1])
			continue

		corpus[str(i)] = page_data

		#get the links and put them into the queue
		try:
			links = page_data[unicode('tropes', "utf-8")]
			for key in links:
				if links[key] not in examined_tropes:
					queue.append(['t', links[key]])
					examined_tropes.append(links[key])
		except:
			exception_ctr_m += 1
			continue

	#except:
		#continue


json_data = json.dumps(corpus)
f = open('corpus.json', 'w')
f.write(json_data)

#useful information
print "links examined:"
print (ext_count)
print "items in corpus"
print (len(corpus.keys()))
print "duplicate tropes detected:"
print (len(examined_tropes))
print "duplicate media detected:"
print (len(examined_media))
print "failed tropes:"
print (len(failed_tropes))
print "failed media:"
print (len(failed_media))
print "exception tropes:"
print (exception_ctr_t)
print "exception media"
print (exception_ctr_m)
#pp.pprint(corpus)
#pp.pprint(page_data)