"""
dumpimages.py
    Downloads all the images on the supplied URL, and saves them to the
    specified output file ("/test/" by default)

Usage:
    python dumpimages.py http://example.com/ [output]
"""
"""
from bs4 import BeautifulSoup as bs
from urllib.request import (
    urlopen, urlparse, urlunparse, urlretrieve)
import os
import sys

def main(url, out_folder="/test/"):
    soup = bs(urlopen(url))
    parsed = list(urlparse(url))

    for image in soup.findAll("img"):
        print("Image: %(src)s" % image)
        filename = image["src"].split("/")[-1]
        parsed[2] = image["src"]
        outpath = os.path.join(out_folder, filename)
        if image["src"].lower().startswith("http"):
            urlretrieve(image["src"], outpath)
        else:
            urlretrieve(urlunparse(parsed), outpath)

def _usage():
    print("usage: python dumpimages.py http://example.com [outpath]")
    
if __name__ == "__main__":
    url = sys.argv[-1]
    out_folder = "/test/"
    if not url.lower().startswith("http"):
        out_folder = sys.argv[-1]
        url = sys.argv[-2]
        if not url.lower().startswith("http"):
            _usage()
            sys.exit(-1)
    main(url, out_folder)
"""

from bs4 import BeautifulSoup
import requests

database = 'https://www.db.yugioh-card.com/yugiohdb/card_search.action?ope=2&cid='

def normal(string):
    return string.replace('\r\n',' ').replace('\n','').replace('\t','')

def singlespaced(string):
    return ' '.join(string.split())

def get(cardnumber):
    webpage = database + str(cardnumber)
    page = requests.get(webpage)
    soup = BeautifulSoup(page.text, "html.parser")
    return soup

def cardname(cardnumber):
    soup = get(cardnumber)
    soup = soup.find("meta", property="og:title")['content']
    soup = soup.replace(' | Card Details | Yu-Gi-Oh! TRADING CARD GAME - CARD DATABASE','')
    return soup

def cardtext(cardnumber):
    soup = get(cardnumber)
    soup = soup.find_all("div", {"class":"item_box_text"})
    return [singlespaced(normal(word.text)) for word in soup]

def carddata(cardnumber):
    soup = get(cardnumber)
    soup = soup.find_all("div", {"class":"item_box"})
    return [singlespaced(normal(word.text)) for word in soup]

print(cardname(15135))
print(cardtext(15135))
print(carddata(15135))
'''
for i in range(4007,4009):
    print(cardname(i))
    print(cardtext(i))
    print(carddata(i))
'''