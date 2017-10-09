import requests
import os
from bs4 import BeautifulSoup
import unicodedata

def getProductCategory(page):
	content = requests.get(page)
	html = content.text
	soup = BeautifulSoup(html)

	for level1 in soup.find_all("div", {'class': 'bucket'}):
		for level2 in level1("div", {'class': 'content'}):
			for level3 in level2("ul"):
				for level4 in level3("li"):
					cat = ""
					for text in level4("a"):
						cat += unicodedata.normalize('NFKD', text.text).encode('ascii','ignore') + ";"
						
					return cat
	