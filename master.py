# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 01:20:19 2020
Card Work - Yu-Gi-Oh
@author: vandr
"""

# alcance = range(4007,15136)
db = 'https://www.db.yugioh-card.com/yugiohdb/card_search.action?ope=2&cid='

# import urllib.request
import numpy as np
import pandas as pd

""" UNUSED
def find_repeat(terms):
    seen = set()
    for word in terms:
        if word in seen:
            return word
        seen.add(word)

duellinks_split = [card.split() for card in duellinks[0:100]]
singles = sorted([word for name in duellinks_split for word in name])
seen = list(set(singles))
test = [word for word in singles if word not in seen]
set(term).intersection(sample[0])
"""

def list_to_txt(your_list,file_name):
    file = pd.DataFrame(your_list, columns=[file_name])
    file.to_csv('outputs/' + file_name + '.txt', index=False, quoting=1)
    
def standarize(text):
    text = text.replace('%21','!')
    text = text.replace('%22','"')
    text = text.replace('%25','%')
    text = text.replace('%26','&')
    text = text.replace('%27',"'")
    text = text.replace('%2C',',')
    text = text.replace('%2D','-')
    text = text.replace('%2E','.')
    text = text.replace('%2F','/')
    text = text.replace('%3A',':')
    text = text.replace('%3B',';')
    text = text.replace('%3F','?')
    text = text.replace('%40','@')
    return text

# cardlists
duellinks = pd.read_csv('comma_separated/duel_links.txt', delimiter=';')
duellinks = [card for card in duellinks['DL'] if ' Token' not in card]
duellinks = sorted(set(duellinks))

serie = pd.read_csv('comma_separated/serie.txt')
archetype = pd.read_csv('comma_separated/archetype.txt')
serie = [term for term in serie]
archetype = [term for term in archetype]
archserie = sorted(set(archetype + serie))

ocg = pd.read_csv('comma_separated/ocg.txt', delimiter=';')
tcg = pd.read_csv('comma_separated/tcg.txt', delimiter=';')
temp = pd.read_csv('comma_separated/temp.txt', delimiter=';')
ocg = [card for card in ocg['OCG'] if ' Token' not in card]
tcg = [card for card in tcg['TCG'] if ' Token' not in card]
temp = [card for card in temp['TEMP'] if ' Token' not in card]
allcards = sorted(set(ocg + tcg + temp))

def search(term):
    return [card for card in allcards if term in card]

###############################################################################
'''
unreleased = [card for card in allcards if card not in duellinks]
unreleased = sorted(set(unreleased))
exclusive = [card for card in duellinks if card not in allcards]
exclusive = sorted(set(exclusive))
tcg_only = [card for card in tcg if card not in ocg]
tcg_only = sorted(set(tcg_only))
ocg_only = [card for card in ocg if card not in tcg]
ocg_only = sorted(set(ocg_only))
'''
###############################################################################
'''
link = pd.read_csv('comma_separated/link_related.txt', delimiter=';')
link = [card for card in link]

pendulum = pd.read_csv('comma_separated/pendulum_related.txt', delimiter=';')
pendulum = [card for card in pendulum]

xyz = pd.read_csv('comma_separated/xyz_related.txt', delimiter=';')
xyz = [card for card in xyz]

mp2 = pd.read_csv('comma_separated/main_phase2.txt', delimiter=';')
mp2 = [card for card in mp2]

restriction = mp2 + link + pendulum + xyz
restriction = sorted(set(restriction))
possible = [card for card in unreleased if card not in restriction]
'''
###############################################################################
'''
duellinks_archserie = [next((lexico for card in duellinks if lexico.lower() in card or lexico in card), None)
                            for lexico in archserie
                            if next((lexico for card in duellinks if lexico.lower() in card or lexico in card), None) != None]

missing_archserie = [lexico for lexico in archserie if lexico not in duellinks_archserie]

archserie_with_restriction = [next((lexico for card in restriction if lexico.lower() in card or lexico in card), None)
                               for lexico in archserie
                               if next((lexico for card in restriction if lexico.lower() in card or lexico in card), None) != None]

free_archserie = [card for card in missing_archserie if card not in archserie_with_restriction]
'''
###############################################################################
'''
card_with_archseries = [card for card in allcards
                         for lexico in archserie
                         if lexico in card or lexico.lower() in card]

card_with_archseries = sorted(set(card_with_archseries))

card_without_archseries = [card for card in allcards if card not in card_with_archseries]
'''
###############################################################################
'''
ocg_archserie = [next((lexico for card in allcards if lexico.lower() in card or lexico in card), None)
                 for lexico in archserie
                 if next((lexico for card in allcards if lexico.lower() in card or lexico in card), None) != None]

anime_only_archserie = [card for card in archserie if card not in ocg_archserie]

not_in_allcards = [card for card in restriction if card not in allcards]
'''
###############################################################################

# from urllib import urlopen
from bs4 import BeautifulSoup
import requests


def get_data(cardname,pagenumber=4007):
    database = 'https://db.ygoprodeck.com/card/?search='
    database = db
    webpage = database + str(pagenumber)
    page = requests.get(webpage)
    soup = BeautifulSoup(page.text, "html.parser")
    return soup

def cardtext(cardname):
    soup = get_data(cardname)
    return soup.find("div", class_="item_box_text")['content']

'''
WORKS SOMETIMES
def cardtext(cardname):
    soup = get_data(cardname)
    return soup.find("meta", property="og:description")['content']
    
def cardimg(cardname):
    soup = get_data(cardname)
    title = soup.find("meta", property="og:title")['content']
    title = title.replace(' - Card Information | Yu-Gi-Oh! Database','').replace(' ','_')
    
    class AppURLopener(urllib.request.FancyURLopener):
        version = "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.69 Safari/537.36"
        
    urllib._urlopener = AppURLopener()
    url = soup.find("meta", property="og:image:secure_url")['content']
    urllib._urlopener.retrieve(url, "C:/Users/vandr/Videos/cards/" + title + ".jpg")
    return url
'''
     
'''
a href="/wiki/A.I.%27s_Ritual" title="A.I.'s Ritual" class="category-page__member-link">A.I.'s Ritual</a>

soup = get_data(duellinks[100])

text = soup.find("meta", property="og:description")
image = soup.find("meta",  property="og:image:secure_url")

import urllib.request
imgURL = "http://site.meishij.net/r/58/25/3568808/a3568808_142682562777944.jpg"

urllib.request.urlretrieve(imgURL, "D:/abc/image/local-filename.jpg")
'''

# page = requests.get(link)
# soup = BeautifulSoup(page.text, 'html.parser')
'''
list_to_txt(duellinks_archserie,'Archseries in Duel Links')
list_to_txt(missing_archserie,'Archseries Missing')

list_to_txt(unreleased,'Duel Links Unreleased')
list_to_txt(exclusive,'Duel Links Exclusive')
'''