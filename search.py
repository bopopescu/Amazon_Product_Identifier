import requests
import os
from bs4 import BeautifulSoup
import unicodedata

def getTitle(page):
	content = requests.get(page)
	html = content.text
	soup = BeautifulSoup(html)


	for level1 in soup.find_all("div", {'id': 'center'}):
		for level2 in level1("div", {'id': 'atfResults'}):
			for level3 in level2("ul"):
				for level4 in level3("li"):
					for aval in level4("a",{'class':'a-link-normal s-access-detail-page  a-text-normal'}):
						link = aval['href']
						for heading in aval("h2"):
							title = str(unicodedata.normalize('NFKD', heading.text).encode('ascii','ignore'))
							return (title, link)
