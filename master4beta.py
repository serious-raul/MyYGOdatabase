# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 08:07:21 2020

@author: vandr
"""

import re
import pandas as pd
import seaborn as sns

def list_to_txt(your_list,file_name):
    file = pd.DataFrame(your_list)
    file.to_csv('outputs/' + file_name + '.txt')
    
def unify(a):
    b = a[['Card Name','Card Type']]
    c = a[['Card Name','Icon']]
    b = b.dropna()
    c = c.dropna()
    c = c.rename(columns={'Icon':'Card Type'})
    d = pd.merge(b, c, how='outer')
    a = a.drop(columns=['Icon','Card Type'])
    a = pd.merge(a, d, how='outer')
    return a

def unify2(a):
    b = a[['Card Name','Level']].dropna()
    c = a[['Card Name','Rank']].dropna()
    d = a[['Card Name','Link']].dropna()
    b = b.rename(columns={'Level':'Level/Rank/Link'})
    c = c.rename(columns={'Rank':'Level/Rank/Link'})
    d = d.rename(columns={'Link':'Level/Rank/Link'})
    e = pd.merge(b, c, how='outer')
    f = pd.merge(e, d, how='outer')
    a = a.drop(columns=['Level','Rank','Link'])
    a = pd.merge(a, f, how='outer')
    return a

###############################################################################
# CONCATENATE LISTS
'''
a = pd.read_csv('outputs/ok/4007 to 4607.txt', delimiter=',')
a['Card Number'] = list(range(4007,4607))
a = unify(a)
# a = unify2(a)

b = pd.read_csv('outputs/ok/4607 to 5207.txt', delimiter=',')
b['Card Number'] = list(range(4607,5207))
b = unify(b)
# b = unify2(b)

c = pd.read_csv('outputs/ok/5207 to 6207.txt', delimiter=',')
c['Card Number'] = list(range(5207,6207))
c = unify(c)
# c = unify2(c)

d = pd.read_csv('outputs/ok/6207 to 7207.txt', delimiter=',')
d['Card Number'] = list(range(6207,7207))
d = unify(d)
# d = unify2(d)

e = pd.read_csv('outputs/ok/7207 to 10207.txt', delimiter=',')
e['Card Number'] = list(range(7207,10207))
e = unify(e)

f = pd.read_csv('outputs/ok/10207 to 15136.txt', delimiter=',')
f = f.dropna(subset=['Card Type'])

g = pd.concat([f,e,d,c,b,a])
# g = unify2(g)
g = g[['Card Number', 'Card Name', 'Level', 'Rank', 'Link', 'Card Text',
       'Status', 'Card Type', 'Pendulum Effect', 'Pendulum Scale',
       'Attribute', 'Monster Type', 'ATK', 'DEF']]

g = g.sort_values(by=['Card Name'])

ocg = g[g['Card Name'] == 'Card information not found.']
ocg.to_csv('outputs/Numbers Not Found.csv', index=False, quoting=0)

db = g[g['Card Name'] != 'Card information not found.']
db.to_csv('outputs/Yugioh - Complete Database.csv', index=False, quoting=0)
'''
###############################################################################
# NORMALIZE THE LISTS
'''
db = pd.read_csv('outputs/Yugioh - Complete Database.csv', delimiter=',')

db['Card Text'] = db['Card Text'].str.replace('^Card Text ','')
db['Card Type'] = db['Card Type'].str.replace('^Card Type ','')
db['Card Type'] = db['Card Type'].str.replace('^Icon ','')
db['Pendulum Effect'] = db['Pendulum Effect'].str.replace('^Pendulum Effect ','')
db['Pendulum Scale'] = db['Pendulum Scale'].str.replace('^Pendulum Scale ','')
db['Attribute'] = db['Attribute'].str.replace('^Attribute ','')
db['Monster Type'] = db['Monster Type'].str.replace('^Monster Type ','')
db['ATK'] = db['ATK'].str.replace('^ATK ','')
db['DEF'] = db['DEF'].str.replace('^DEF ','')
db['Level'] = db['Level'].str.replace('^Level ','')
db['Rank'] = db['Rank'].str.replace('^Rank ','')
db['Link'] = db['Link'].str.replace('^Link ','')

db['Pendulum Scale'] = pd.to_numeric(db['Pendulum Scale'], errors='coerce')
db['Level'] = pd.to_numeric(db['Level'], errors='coerce')
db['Rank'] = pd.to_numeric(db['Rank'], errors='coerce')
db['Link'] = pd.to_numeric(db['Link'], errors='coerce')
db['ATK'] = pd.to_numeric(db['ATK'], errors='coerce')
db['DEF'] = pd.to_numeric(db['DEF'], errors='coerce')

db['Card Text'] = db['Card Text'].str.replace(' Forbidden$', '')
db['Card Text'] = db['Card Text'].str.replace(' Limited$', '')
db['Card Text'] = db['Card Text'].str.replace(' Semi-limited$', '')

for i in a.index:
    if 'Spell' not in db['Card Type'][i] and 'Trap' not in db['Card Type'][i]:
        db['Card Type'][i] = db['Card Type'][i] + ' Monster'

db.to_csv('outputs/Yugioh - Ultimate Database.csv', index=False)
'''
###############################################################################
# BUILT MY ARCHETYPES

db = pd.read_csv('outputs/Yugioh - Ultimate Database.csv')
db = db[~db['Card Text'].str.contains('This card is not treated')]
db = db.reset_index()
db = db.drop(columns=['index'])

def firstword(string):
    if ' ' in string:
        return string[:string.index(' ')]
    if '.' in string:
        return string[:string.index('.')]
    if ')' in string:
        return string[:string.index(')')]
    else: return ''

def secondword(string):
    string = string[len(firstword(string))+1:]
    return firstword(string)

def find(df,index):
    name = df['Card Name'][index]
    effect = df['Card Text'][index]
    effect = effect.replace('"' + name + '"','')
    try:
        string = re.search('"(.+?)"', effect).group(1)
        # after = df['Card Text'][index].partition('"' + string + '" ')[2]
        endofstring = db['Card Text'][index].index('"' + string + '"')  + len('"' + string + '"') + 1
        after = db['Card Text'][index][endofstring:]
        # after = after.split(' ')[1:2][0].capitalize()
        return (string, after)
    except AttributeError:
        # nothing found in the original string
        pass # apply error handling

trial = set([find(db,i) for i in db.index])
trial = pd.DataFrame(trial,columns=['Archetype','Aftermaths'])
trial = trial[trial['Aftermaths'].str.len() >= 1]
trial = trial[~trial['Archetype'].str.contains(' Token')]
trial['Aftermaths'] = trial['Aftermaths'].str.replace('^cards in your ','')
trial['Aftermaths'] = trial['Aftermaths'].str.replace('^card in your ','')
trial['Aftermaths'] = trial['Aftermaths'].str.replace('^cards to your ','')
trial['Aftermaths'] = trial['Aftermaths'].str.replace('^card to your ','')
trial['Aftermaths'] = trial['Aftermaths'].str.replace('^cards from your ','')
trial['Aftermaths'] = trial['Aftermaths'].str.replace('^card from your ','')
trial['Aftermaths'] = trial['Aftermaths'].str.replace('^card is in your ','')
'''
archetype = trial.sort_values('Archetype')
archetype = archetype[~archetype['Archetype'].str.contains('!etanimretxE !etacidarE !etanimilE')]
# archetype.to_csv('outputs/scrap_archetypes.txt',index=False)
'''
###############################################################################
# GETTING THE RESTRICTIONS (WHICH CARD TYPES EACH ARCHETYPE SUPPORTS)

clean = [(trial['Archetype'][i],firstword(trial['Aftermaths'][i]) + ' ' + secondword(trial['Aftermaths'][i]))for i in trial.index]
clean = pd.DataFrame(clean,columns=['Archetype','Restriction']).drop_duplicates()
clean['Restriction'] = clean['Restriction'].str.replace('^Pendulum Zone','Pendulum Monster')
clean['Restriction'] = clean['Restriction'].str.replace('^Spell &','Spell/Trap')

# THESE ARE ALL TYPES OF CARDS MENTIONED IN OTHER CARDS ALONGSIDE ARCHETYPES
mentions = ['Effect Monster', 'Fusion Monster', 'Link Monster', 'Pendulum Monster',
            'Ritual Monster', 'Xyz Monster', 'Synchro Monster', 'Normal Monster', 
            'Normal Spell', 'Normal Trap', 'Quick-Play Spell', 'Ritual Spell',
            'Continuous Spell', 'Equip Spell', 'Field Spell', 'Equip Card',
            'Spell/Trap', 'Tuner', 'monster', 'Monster', 'Spell', 'Trap',
            'card', 'Card']

def correct(string): return next((ment for ment in mentions if ment in string), None)

archetypeList = [(clean['Archetype'][i],correct(clean['Restriction'][i])) for i in clean.index]
archetypeList = pd.DataFrame(archetypeList,columns=['Archetype','Restriction']).drop_duplicates()
archetypeList = archetypeList.dropna()

archetypeList['Restriction'] = archetypeList['Restriction'].str.title()
# archetypeList = archetypeList[archetypeList['Restriction'] != 'Card']

archetypeList2 = archetypeList[archetypeList['Restriction'] == 'Monster']
archetypeList3 = archetypeList[archetypeList['Restriction'] != 'Monster']
archetypeList4 = archetypeList2[~archetypeList2.Archetype.isin(archetypeList3.Archetype)]
archetypeList4['Restriction'] = 'Spell/Trap'
archetypeList = pd.concat([archetypeList,archetypeList4])

archetypeList = archetypeList.sort_values('Archetype')
archetypeList = archetypeList.reset_index()
archetypeList = archetypeList.drop(columns=['index'])
archetypeList = archetypeList.drop_duplicates()

###############################################################################
# COUNTING ARCHETYPES WITH RESTRICTIONS

def search(df,index):
    name = df['Card Name'][index]
    effect = df['Card Text'][index]
    effect = effect.replace('"' + name + '"','')
    try:
        string = re.search('"(.+?)"', effect).group(1)
        cardtype = db['Card Type'][index]
        return (string, cardtype)
    except AttributeError:
        # nothing found in the original string
        pass # apply error handling

newlist = [search(db,i) for i in db.index if search(db,i) != None]
newlist = pd.DataFrame(newlist,columns=['Archetype','Restriction'])
newlist2 = newlist.groupby(['Archetype','Restriction']).size().reset_index(name='Count')

def checkfor(string,df,**kwargs):
    restriction = kwargs.get("restriction") #TRUE OR FALSE
    case = kwargs.get("case") #TRUE OR FALSE
    regex = kwargs.get("regex") #TRUE OR FALSE
    if restriction:
        restriction = restriction.split(' ')
        if len(restriction) == 2:
            data = df[df['Card Type'].str.contains(restriction[0],case=case,regex=regex) &
                      df['Card Type'].str.contains(restriction[1],case=case,regex=regex)]
        if len(restriction) == 1:
            data = df[df['Card Type'].str.contains(restriction[0],case=case,regex=regex)]
        if restriction[0] == 'Spell/Trap':
            restriction = restriction[0].split('/')
            data = df[df['Card Type'].str.contains(restriction[0],case=case,regex=regex) |
                      df['Card Type'].str.contains(restriction[1],case=case,regex=regex)]
        if restriction[0] == 'Card':
            data = df
        else:
            return df[df['Card Name'].str.contains(string,case=case,regex=regex) |
                      df['Card Text'].str.contains('"' + string + '"',case=case,regex=regex) |
                      df['Pendulum Effect'].str.contains('"' + string + '"',case=case,regex=regex)]
        
        return data[data['Card Name'].str.contains(string,case=case,regex=regex) |
                    data['Card Text'].str.contains('"' + string + '"',case=case,regex=regex) |
                    data['Pendulum Effect'].str.contains('"' + string + '"',case=case,regex=regex)]

    else:
        return df[df['Card Name'].str.contains(string,case=case,regex=regex) |
                  df['Card Text'].str.contains('"' + string + '"',case=case,regex=regex) |
                  df['Pendulum Effect'].str.contains('"' + string + '"',case=case,regex=regex)]

counting = [{'Title':archetypeList['Archetype'][i],
             'Restriction':archetypeList['Restriction'][i],
             'Count':len(set(checkfor(archetypeList['Archetype'][i],db,case=True,regex=False,restriction=archetypeList['Restriction'][i]).index))}
             for i in archetypeList.index]

count = pd.DataFrame(counting)
count = count[count['Count'] >= 1]
count = count.sort_values('Count', ascending=False)
count = count.reset_index()
count = count.drop(columns=['index'])
count['Restriction'] = count['Restriction'].str.replace('Card','None')

###############################################################################
# COUNT ARCHETYPES
'''
db = pd.read_csv('outputs/Yugioh - Ultimate Database.csv')

for i in db.index:
    if 'Normal Monster' in db['Card Type'][i]:
        db.at[i,'Card Text'] = '#'

archetype = pd.read_csv('outputs/scrap_archetypes.txt')

# ygopordeck_archetype = pd.read_csv('comma_separated/prodeck/archetypes.txt')

def checkfor(string,df,**kwargs):
    regex = kwargs.get("regex")
    case = kwargs.get("case")
    return df[df['Card Name'].str.contains(string,case=case,regex=regex) |
              df['Card Text'].str.contains('"' + string + '"',case=case,regex=regex) |
              df['Pendulum Effect'].str.contains('"' + string + '"',case=case,regex=regex)]

counting = [{'Title':string,'Count':len(set(checkfor(string,db,case=True,regex=False).index))} for string in archetype['Archetype']]
count = pd.DataFrame(counting).sort_values('Count', ascending=False)
count = count.reset_index()
count = count.drop(columns=['index'])
'''
###############################################################################
# COUNT VALUES
'''
ocg = pd.read_csv('outputs/Numbers Not Found.csv')
db = pd.read_csv('outputs/Yugioh - Ultimate Database.csv')

b = pd.DataFrame(db['Card Type'].value_counts())
c = pd.DataFrame(db['Level'].value_counts())
d = pd.DataFrame(db['Rank'].value_counts())
e = pd.DataFrame(db['Link'].value_counts())
f = pd.DataFrame(db['Attribute'].value_counts())
g = pd.DataFrame(db['Monster Type'].value_counts())
h = pd.DataFrame(db['ATK'].value_counts())
j = pd.DataFrame(db['DEF'].value_counts())

classe = [i for i in b.index if b['Card Type'][i] <= 2]
[db[db['Card Type'] == classe[i]]['Card Name'] for i,_ in enumerate(classe)]
'''
###############################################################################
# CROSSTALBES
'''
db = pd.read_csv('outputs/Yugioh - Ultimate Database.csv', delimiter=',')

# k = pd.crosstab(db['Attribute'],db['Monster Type'])

# low = list(db['Card Name'])
# miss = [card for card in tcg if card not in low]
'''
###############################################################################

print('Done!')