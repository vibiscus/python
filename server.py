import cherrypy
import pymysql
from jinja2 import Environment, FileSystemLoader

import cherrypy, os
import requests
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from wordcloud import WordCloud
from urllib.parse import urlparse
from lxml import etree
import mysql.connector
import requests
import time


env = Environment(loader=FileSystemLoader('templates'))

class HelloWorld(object):
        def index(self):
            tmpl = env.get_template('index.html')
            return tmpl.render()

        def resultat(self, url = None):

            # ====================== TRAITEMENT URL ======================
            # vérifier que c'est une url
            #vérifier que l'url est valide


            #vérifier que la saisie commence par https://www.zalando.fr
            o = urlparse(url)
            if(o.hostname == None):
                erreur = "Ceci n'est pas une url. Veuillez recommencer."
                tmpl = env.get_template('error.html')
                return tmpl.render(e=erreur)
            saisie = "https://" +o.hostname
            zalando ="https://www.zalando.fr"
            if saisie == zalando:
                r = requests.get(url)
                if r.status_code == 200:
                    print('Web site exists')
                    soup = BeautifulSoup(r.content, "lxml")

                    chaine = ""
                    #prendre la balise reviewDescriptionText (celles où il y a les commentaires)
                    g_data = soup.find_all("p", {"class": "reviewDescriptionText"})
                    for data in g_data:
                        chaine += data.text

                    #éliminer les caractères autres que des mots
                    chaine = chaine.replace('.', '')
                    chaine = chaine.replace(',', '')
                    chaine = chaine.replace('!', '')
                    chaine = chaine.lower()
                    newlist = chaine.split()


                    # ====================== TRI DU TEXTE ======================

                    dico_poubelle = open("dico_poubelle.txt").read().splitlines()
                    dico_positifs = open("dico_positifs.txt").read().splitlines()
                    dico_negatifs = open("dico_negatifs.txt").read().splitlines()

                    # on enlève les mots de la liste poubelle --> on obtient malistefinale
                    malistefinale = [i for i in newlist if i not in dico_poubelle]

                    i =0
                    j =0
                    k =0
                    tab_positif = []
                    tab_negatif = []
                    tab_neutre = []

                    # création de trois nouveaux tableaux : mots positifs et négatifs trouvés dans les dictionnaires
                    # les mots non trouvés se retrouvent dans le tableau neutre
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

                    # affichage des tableaux obtenus
                    print(tab_positif)
                    print(i)
                    print(tab_negatif)
                    print(j)
                    print(tab_neutre)
                    print(k)

                    # ====================== GRAPHIQUE "+" / "-" ======================

                    # calcul de la proportion des mots positifs et négatifs
                    proportionPositif = (i*100)/(i+j)
                    proportionNegatif = (j*100)/(i+j)

                    name = ['positif', 'négatif']
                    data = [proportionPositif, proportionNegatif]

                    explode=(0, 0.15)
                    plt.pie(data, labels=name, autopct='%1.1f%%', startangle=90, colors="gr")
                    plt.axis('equal')
                    plt.axis("off")
                    # sauvegarde graphique obtenu
                    plt.savefig('templates/graph.png')
                    # clear pour éviter erreur dans affichage
                    plt.clf()

                    # ======================== WORD CLOUD ==========================

                    wordcloud = WordCloud().generate(chaine)
                    # Open a plot of the generated image.
                    plt.imshow(wordcloud)
                    plt.axis("off")

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
                    # Open a plot of the generated image
                    plt.imshow(wordcloud)
                    plt.axis("off")
                    # sauvegarde du word cloud obtenu
                    plt.savefig('templates/wc.png')
                    # clear pour éviter erreur dans affichage
                    plt.clf()

                    # ======================== CRÉATION XML ==========================

                    dicos = etree.Element("Dictionnaires")

                    # prend toutes les balises neutre
                    for neutre_data in tab_neutre:
                        motneutre = etree.SubElement(dicos, "motneutre")
                        motneutre.text = neutre_data

                    # prend toutes les balises positif
                    for pos_data in tab_positif:
                        motpos = etree.SubElement(dicos, "motpos")
                        motpos.text = pos_data

                    # prend toutes les balises négatif
                    for neg_data in tab_negatif:
                        motneg = etree.SubElement(dicos, "motneg")
                        motneg.text = neg_data

                    print(etree.tostring(dicos, pretty_print=False))
                    var = etree.tostring(dicos, pretty_print=False)
                    var2= str(var)
                    file = open("dico.xml", "w" , encoding="utf-8")
                    file.write(var2)
                    file.close()

                    # ======================== stockage BDD ==========================
                    # connexion à la BDD
                    w = o.netloc + o.path
                    conn = mysql.connector.connect(host='localhost',database='Python', user='root', password='root', port = 8889 )
                    cursor = conn.cursor(pymysql.cursors.DictCursor)
                    filedb = open('dico.xml', 'r')
                    file_content = filedb.read()
                    filedb.close()
                    # insérer url + contenu du xml dans la BDD
                    t = time.strftime("%d/%m/%Y")
                    print (t)
                    # update clé primaire composée phpmyadmin
                    cursor.execute("INSERT INTO WebExtractor(url, date, xml) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE "
                                   "xml = %s",  (w, t, file_content, file_content))
                    conn.commit()
                    cursor.close()
                    conn.close()

                    tmpl = env.get_template('resultat.html')
                    return tmpl.render(url=url)
                else:
                    erreur = "L'url n'existe pas. Veuillez recommencer."
                tmpl = env.get_template('error.html')
                return tmpl.render(e=erreur)

            # si url saisie n'existe pas : page erreur
            else:
                erreur = "Ceci n'est pas une url zalando. Veuillez recommencer."
                tmpl = env.get_template('error.html')
                return tmpl.render(e=erreur)
                error.exposed = True
        index.exposed = True
        resultat.exposed = True

cherrypy.config.update({"tools.staticdir.root":os.getcwd()})
cherrypy.quickstart(HelloWorld(), config='server.conf')
