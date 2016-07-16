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

env = Environment(loader=FileSystemLoader('templates'))

class HelloWorld(object):
        def index(self):
            tmpl = env.get_template('index.html')
            return tmpl.render()

        def resultat(self, url = None):

            # ====================== TRAITEMENT URL ======================

            o = urlparse(url)
            saisie = "https://" +o.hostname
            zalando ="https://www.zalando.fr"
            if saisie == zalando:
                r = requests.get(url)
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


                # ====================== TRI DU TEXTE ======================

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

                # ====================== GRAPHIQUE "+" / "-" ======================

                proportionPositif = (i*100)/(i+j)
                proportionNegatif = (j*100)/(i+j)

                name = ['positif', 'négatif']
                data = [proportionPositif, proportionNegatif]

                print("Proportion d'avis positifs et négatifs")
                explode=(0, 0.15)
                plt.pie(data, labels=name, autopct='%1.1f%%', startangle=90, colors="gr")
                plt.axis('equal')
                plt.axis("off")
                plt.savefig('templates/graph.png')

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
                plt.savefig('templates/wc.png')

                # ======================== CRÉATION XML ==========================

                dicos = etree.Element("Dictionnaires")

                for neutre_data in tab_neutre:
                    motneutre = etree.SubElement(dicos, "motneutre")
                    motneutre.text = neutre_data

                for pos_data in tab_positif:
                    motpos = etree.SubElement(dicos, "motpos")
                    motpos.text = pos_data

                for neg_data in tab_negatif:
                    motneg = etree.SubElement(dicos, "motneg")
                    motneg.text = neg_data

                print(etree.tostring(dicos, pretty_print=True))
                var = etree.tostring(dicos, pretty_print=True)
                var2= str(var)
                file = open("dico.txt", "w" , encoding="utf-8")
                file.write(var2)
                file.close()

                tmpl = env.get_template('resultat.html')
                return tmpl.render(url=url)

                 # ======================== stockage BDD ==========================

                w = str(o)
                conn = mysql.connector.connect(host='localhost',database='Python', user='root', password='root', port = 8889 )
                cursor = conn.cursor(pymysql.cursors.DictCursor)
                filedb = open('/dico.txt', 'r')
                file_content = file.read()
                file.close()
                #cursor.execute("INSERT INTO WebExtractor(url, xml) VALUES (%s, %s)",  (w, file_content))
                #query = "INSERT INTO testpython VALUES (%s)"
                #cursor.execute(query, (file_content,))
                conn.commit()
                cursor.close()
                conn.close()

            #else:
                 #def error(self):
                    #tmpl = env.get_template('error.html')
                    #return tmpl.render()
            #error.exposed = True
        index.exposed = True
        resultat.exposed = True
cherrypy.config.update({"tools.staticdir.root":os.getcwd()})
cherrypy.quickstart(HelloWorld(), config='server.conf')
