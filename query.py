# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 21:19:33 2020

@author: vandr
"""

import requests
from bs4 import BeautifulSoup

# Collect first page of artists’ list
main_phase_2 = 'https://db.ygoprodeck.com/search/?&fname=main%20phase%202&desc=main%20phase%202&num=30&offset=0&view=List'

page_number = range(1,5)
link = 'https://www.db.yugioh-card.com/yugiohdb/card_search.action?ope=1&sess=1&keyword=link&stype=2&ctype=&starfr=&starto=&pscalefr=&pscaleto=&linkmarkerfr=&linkmarkerto=&atkfr=&atkto=&deffr=&defto=&othercon=2'
contact = 'https://db.ygoprodeck.com/card/?search=A.I.%20Contact'

box1 = 'http://duellinks.gamea.co/c/3zwdkbj1'

page = requests.get(contact)
soup = BeautifulSoup(page.text, 'html.parser')

# last_links = soup.find(class_='AlphaNav')
# last_links.decompose()

# artist_name_list = soup.find(class_='BodyText')
# artist_name_list_items = soup.find_all('a')

# for artist_name in artist_name_list_items:
    # names = artist_name.contents[0]
    # print(names)

"""
var x = document.querySelectorAll("a");
var myarray = []
for (var i=0; i<x.length; i++){
var nametext = x[i].textContent;
var cleantext = nametext.replace(/\s+/g, ' ').trim();
var cleanlink = x[i].href;
myarray.push([cleantext,cleanlink]);
};
function make_table() {
    var table = '<table><thead><th>Name</th><th>Links</th></thead><tbody>';
   for (var i=0; i<myarray.length; i++) {
            table += '<tr><td>'+ myarray[i][0] + '</td><td>'+myarray[i][1]+'</td></tr>';
    };
 
    var w = window.open("");
w.document.write(table); 
}
make_table()
"""
