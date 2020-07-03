# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 17:32:18 2020

@author: vandr
"""

from bs4 import BeautifulSoup
import requests
import pandas as pd

database = 'https://www.db.yugioh-card.com/yugiohdb/card_search.action?ope=2&cid='
avaliable_languages = ['ja','en','de','fr','it','es','pt','ko']
card_range = range(4007,15136)

def clean(string):
    return string.replace(' | Card Details | Yu-Gi-Oh! TRADING CARD GAME - CARD DATABASE','')

def normal(string):
    return string.replace('\r\n',' ').replace('\n',' ').replace('\t',' ')

def singlespaced(string):
    return ' '.join(string.split())

def get(card_number,local='en'):
    webpage = database + str(card_number) + '&request_locale=' + local
    page = requests.get(webpage)
    soup = BeautifulSoup(page.text, "html.parser")
    return soup

def cardname(card_number,local='en'):
    soup = get(card_number,local)
    soup = soup.find("meta", property="og:title")['content']
    print(card_number)
    if clean(soup) == 'none':
        return {'Card Name':'Card information not found.'}
    else:
        return {'Card Name':soup}

def cardlimit(card_number,local='en'):
    main = get(card_number,local)
    soup = main.find("div", {"class":"forbidden_limited limited_type_1"})
    if soup is None:
        soup = main.find("div", {"class":"forbidden_limited limited_type_2"})
        if soup is None:
            soup = main.find("div", {"class":"forbidden_limited limited_type_3"})
    if soup is None:
        return {'Status':'Unlimited'}
    else:
        return {'Status':singlespaced(normal(soup.text))}

def carddata(card_number,local='en'):
    main = get(card_number,local)
    key = main.find_all("span", {"class":"item_box_title"})
    key_list = [singlespaced(normal(word.text)).replace('Icon','Card Type') for word in key]
    value = main.find_all("div", {"class":"item_box"})
    value_list = [singlespaced(normal(word.text)) for word in value]
    return dict(zip(key_list,value_list))

def cardeffect(card_number,local='en'):
    main = get(card_number,local)
    key = main.find_all("div", {"class":"item_box_title"})
    key_list = [singlespaced(normal(word.text)) for word in key]
    value = main.find_all("div", {"class":"item_box_text"})
    value_list = [singlespaced(normal(word.text)) for word in value]
    if len(value_list) == 0:
        return {'Card Text':'Card information not found.'}
    else:
        return dict(zip(key_list,value_list))

def list_to_txt(your_list,file_name):
    file = pd.DataFrame(your_list)
    file.to_csv('outputs/ok/' + file_name + '.txt', index=False)

# Test = [print(cardname(i)) for i in card_range[0:10]]
# list_to_txt(Test,'All OCG and TCG Cards')

# List = [dict({'Card Number':i},**cardname(i),**cardlimit(i),**cardeffect(i),**carddata(i)) for i in range(10207,15136)]
# file = pd.DataFrame(List)
# list_to_txt(file,'10207 to 15136')
print('DONE!!')