        # -*- coding: utf-8 -*-
import cherrypy
import requests
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
from bs4 import BeautifulSoup
from wordcloud import WordCloud, STOPWORDS
#import matplotlib as inline
from wordcloud import WordCloud
import re


# vérifier format URL Zalando
# vérifier si dans BDD
# si dans BDD + si même jour alors récupérer infos
# sinon :
r = requests.get("https://www.zalando.fr/adidas-originals-gazelle-baskets-basses-ad111s0af-a11.html")

soup = BeautifulSoup(r.content, "lxml")

chaine = ""
g_data = soup.find_all("p", {"class": "reviewDescriptionText"}) #prendre la balise reviewDescriptionText
for data in g_data:
    chaine += data.text

chaine = chaine.replace('.', '')
chaine = chaine.replace(',', '')
chaine = chaine.replace('!', '')
chaine = chaine.lower()
newlist = chaine.split()

# Mettre les dictionnaires (fichiers) dans des tableaux : poubelle, positif, négatif
# attention maj/min

dico_poubelle = open("dico_poubelle.txt").read().splitlines()
dico_positifs = open("dico_positifs.txt").read().splitlines()
dico_negatifs = open("dico_negatifs.txt").read().splitlines()

# on enlève les mots de la liste poubelle --> on obtient malistefinale
malistefinale = [i for i in newlist if i not in dico_poubelle]

#print (malistefinale)

i =0
j =0
k =0
tab_positif = []
tab_negatif = []
tab_neutre = []

for mot in malistefinale:
    if mot in dico_positifs:
        tab_positif.append(mot)
        i+=1
    elif mot in dico_negatifs:
        tab_negatif.append(mot)
        j+=1
    elif mot not in dico_poubelle:
        tab_neutre.append(mot)
        k+=1

print(tab_positif)
print(i)
print(tab_negatif)
print(j)
print(tab_neutre)
print(k)

proportionPositif = (i*100)/(i+j)
proportionNegatif = (j*100)/(i+j)
# tauxFiabilite = ??
# print("Le taux de fiabilité de l'analyse est de " tauxFiabilite " %")

# génération du graphique "+" vs "-"
name = ['positif', 'négatif']
#data = [proportionPositif, proportionNegatif]
data = [40, 20]

print("Proportion d'avis positifs et négatifs")
explode=(0, 0.15)
plt.pie(data, labels=name, autopct='%1.1f%%', startangle=90, colors="gr")
plt.axis('equal')
plt.show()

# gération du wordcloud
wordcloud = WordCloud().generate(chaine)
# Open a plot of the generated image.
plt.imshow(wordcloud)
plt.axis("off")

#split a document to words
#text_1 = re.split(r'[\n.()!, ""/]', chaine)
# delete some empty string
#text_2 = [x for x in text_1 if len(x) > 0]
# get word frequency and delete some stopwords
wg = newlist
wd = {}
for w in wg:
    if w in dico_poubelle:
        continue
    else:
        str(w)
        if w not in wd:
            wd[w] = 1
        else:
            wd[w] += 1

# get the wordcloud
wordcloud = WordCloud().generate_from_frequencies(wd.items())
# Open a plot of the generated image.
plt.imshow(wordcloud)
plt.axis("off")
plt.show()
