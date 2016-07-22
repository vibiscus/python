# Guide 

# Lancement du programme
Au lancement du programme, la page html s'affiche.
L'utilisateur saisit une url et clique sur Entrer.

# Traitement des données.
La page des résultats de l'analyse s'affiche. 

1. Si l'url est bien une url d'un produit du site Zalando, alors le graphique et le wordcloud apparaissent. 
2. Si l'url n'est pas une url du site Zalando, alors le message "Ceci n'est pas une url zalando. Veuillez recommencer." apparait.
3. Si l'url n'existe pas, alors le message "L'url n'existe pas. Veuillez recommencer." apparait. 
4. Si la saisie n'est pas une url, alors le message "Ceci n'est pas une url. Veuillez recommencer." apparait.

Il faut que l'url du site Zalando soit bien celle d'un produit pour pouvoir analyser les commentaires : les pages du type accueil Zalando, contact ou mentions légales ne sont pas gérées par le programme.

Dans la base de données sont récupérées l'url, la date du jour et le contenu des commentaires sous format xml. 
url et date étant la clé primaire composée, à chaque fois l'utilisateur saisit la même url le même jour, les éventuels commentaires 
supplémentaires sont ajoutés (update) dans xml (pas de nouvelle ligne créée).

La fiabilité de l'analyse des commentaires dépend de l'exhaustivité des dictionnaires (de mots positifs, négatifs et de la liste poubelle).
