__author__ = 'hannahprovenza'
from bs4 import BeautifulSoup, SoupStrainer
import lxml
import requests

def run_trope_scraper(my_url):

    try:
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
        page_data["type"] = "trope"

        #subdict for links to media
        page_data["links"] = {}
        #creates list of categories
        category_list = []
        for media_category in soup.find_all("div", class_="folderlabel", ):
            category_list.append(media_category.get_text().strip())
        category_list.remove(category_list[0])

        # Makes a dictionary mapping each media category to a dictionary mapping titles to URLs
        # {category: {title: URL, title2: URL2}
        for media_category, media_details in zip(category_list, soup.find_all("div", class_="folder")):
            page_data["links"][media_category] = {}
            for list_item in media_details.find_all('li'):
                try:
                    link = list_item.find('a')
                    #the following if condition makes sure that we only get media titles and not links to other tropes
                    if link.get('href').startswith('http://tvtropes.org') and not link.get('href').startswith('http://tvtropes.org/pmwiki/pmwiki.php/Main'):
                        page_data["links"][media_category][link.get_text().replace(".", "")] = link.get('href')
                # the exceptions cover some cases where there's an a with no href
                except TypeError:
                    continue
                except AttributeError:
                    continue

        return page_data

    except:
        return None

if __name__=="__main__":
    import pprint
    
    page_data = run_trope_scraper('http://tvtropes.org/pmwiki/pmwiki.php/Main/SignificantGreenEyedRedhead')    # Use the following three lines to preview output with prettyprint
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(page_data)