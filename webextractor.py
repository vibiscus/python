# -*- coding: utf-8 -*-
import cherrypy
import requests
from bs4 import BeautifulSoup

page = \
"""
<html>
	<head>
	    <meta charset="utf-8" />
		<title> Web Extractor </title>
		<link rel="stylesheet" href="css/style.css" >
	</head>
	<body>
        <form  action="recup" method="POST">
		    <fieldset>
		        <input placeholder="Entrez votre URL : " name="url" id="url"/><br/>
			</fieldset>
			<p><input type="submit" value="Valider"></p>	<!--target="_blank" pour une autre page-->
		</form>
    </body>
</html>
"""

page2 = \
"""
<html>
    <head>
        <meta charset="utf-8" />
        <title>Page interactive </title>
    </head>
    <body>

    </body>
</html>
"""

class WEBEX(object):
    @cherrypy.expose
    def index(self):
        return page

    @cherrypy.expose
    def recup(self,url):
        r = requests.get(url)

        soup = BeautifulSoup(r.content)

        links = soup.find_all("a")
        for link in links:
            print("<a href='%s'>%s</a>" %(link.get("href"), link.text))

        g_data = soup.find_all("p", {"class": "reviewDescriptionText"}) #prendre la balise reviewDescriptionText

        texts = ''
        texts2 = ''
        for item in g_data:
            texts = texts + ' ' + item.text #afficher uniquement le texte contenu dans la balise

        texts2 = texts.lower()

        #print(texts)

        # Mettre les dictionnaires (fichiers) dans des tableaux : poubelle, positif, négatif
        # attention maj/min

        ## Poubelle
        dicoPoubelle = open("dico_poubelle.txt")
        dico_poubelle = []
        for word in dicoPoubelle:
            dico_poubelle.append(word.strip())

        print(dico_poubelle)
        dicoPoubelle.close()


        ## Positif
        dicoPositifs = open("dico_positifs.txt")
        dico_positifs = []
        for word in dicoPositifs:
            dico_positifs.append(word.strip())

        print(dico_positifs)
        dicoPositifs.close()

        ## Négatif
        dicoNegatifs = open("dico_negatifs.txt")
        dico_negatifs = []
        for word in dicoNegatifs:
            dico_negatifs.append(word.strip())

        print(dico_negatifs)
        dicoNegatifs.close()

        cpt  =0
        i =0
        j =0
        k =0
        tab_positif = []
        tab_negatif = []
        tab_neutre = []

        for mot in texts2.split(" "):
            if mot in dico_positifs:
                tab_positif.append(mot)
                i+=1
            elif mot in dico_negatifs:
                tab_negatif.append(mot)
                j+=1
            elif mot not in dico_poubelle:
                tab_neutre.append(mot)
                k+=1

        return tab_neutre

cherrypy.quickstart(WEBEX()) #,config 'nom_fichier' pour stocker la configuration de la connexion)
