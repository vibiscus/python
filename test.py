        # -*- coding: utf-8 -*-
import cherrypy
import requests
from bs4 import BeautifulSoup

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
