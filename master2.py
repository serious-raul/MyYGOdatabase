# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 22:57:03 2020
Card Work
@author: vandr
"""

from bs4 import BeautifulSoup
import requests
import pandas as pd

database = 'https://www.db.yugioh-card.com/yugiohdb/card_search.action?ope=2&cid='
english = '&request_locale=en'
portuguese = '&request_locale=pt'
japanese = '&request_locale=ja'
card_range = range(4007,15136)

def clean(string):
    return string.replace(' | Card Details | Yu-Gi-Oh! TRADING CARD GAME - CARD DATABASE','')

def normal(string):
    return string.replace('\r\n',' ').replace('\n','').replace('\t','')

def singlespaced(string):
    return ' '.join(string.split())

def get(card_number):
    webpage = database + str(card_number)
    page = requests.get(webpage)
    soup = BeautifulSoup(page.text, "html.parser")
    return soup

def cardname(card_number):
    soup = get(card_number)
    soup = soup.find("meta", property="og:title")['content']
    print(card_number)
    if soup is not None:
        return clean(soup)
    else:
        return 'Card information not found.'

def cardtext(card_number):
    soup = get(card_number)
    soup = soup.find("div", {"class":"item_box_text"})
    if soup is not None:
        return singlespaced(normal(soup.text))
    else:
        return 'Card information not found.'

def cardlimit(card_number):
    main = get(card_number)
    soup = main.find("div", {"class":"forbidden_limited limited_type_1"})
    if soup is None:
        soup = main.find("div", {"class":"forbidden_limited limited_type_2"})
        if soup is None:
            soup = main.find("div", {"class":"forbidden_limited limited_type_3"})
    if soup is None:
        return 'Card information not found.'
    else:
        return singlespaced(normal(soup.text))

def carddata(card_number):
    main = get(card_number)
    soup = main.find_all("div", {"class":"item_box"})
    if soup is not None:
        return [singlespaced(normal(word.text)) for word in soup]
    else:
        return 'Card information not found.'

def list_to_txt(your_list,file_name):
    file = pd.DataFrame(your_list)
    file.to_csv('outputs/' + file_name + '.txt', index=False, quoting=1)

# pool = pd.DataFrame(columns=['Name','Text','Attribute','Level/Rank/Link','Card Type','Secondary Type','ATK','DEF','Pendulum Scale'])

# Name = [print(cardname(i)) for i in card_range[0:10]]
# list_to_txt(Name,'All OCG and TCG Cards')

# List = [[i,cardname(i),cardtext(i),*carddata(i)] for i in range(4007,4036)]