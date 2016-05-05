from bs4 import BeautifulSoup, SoupStrainer
import lxml
import requests

def run_media_scraper(my_url):

    #try:
        url = my_url
        html_doc = requests.get(url)
        soup = BeautifulSoup(html_doc.content, 'lxml')

        #this is where we put the information we scrape
        page_data = {}

        #article text
        page_data["text"] = soup.find("div", class_="page-content").get_text()

        #title string
        page_data["title"] = soup.title.string

        #indicating if this is a trope or media link
        page_data["type"] = "media"

        #creates list of categories
        category_list = []

        trope_map = {}

        for tropes in soup.find_all("a", class_="twikilink", ):
            href = tropes.get('href')
            clean = href.strip()

            if (clean).startswith('/pmwiki/pmwiki.php'):
                clean = 'http://tvtropes.org' + clean

            #make sure we don't insert any non-trope links
            if (clean).startswith('http://tvtropes.org') and not (clean).startswith('http://tvtropes.org/pmwiki/pmwiki.php/Main'):
                continue

            trope_map[tropes.string.replace(".", "")] = clean

        page_data["tropes"] = trope_map

        return page_data

if __name__=="__main__":
    import pprint
    
    page_data = run_media_scraper('http://tvtropes.org/pmwiki/pmwiki.php/Literature/HarryPotter')    # Use the following three lines to preview output with prettyprint
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(page_data)