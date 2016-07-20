# Guide utilisateur 

L'utilisateur saisit une url et clique sur Entrer.
Une nouvelle page s'affiche: 
1. Si l'url est bien une url d'un produit du site Zalando, alors le graphique et le wordcloud apparaissent.
2. Si l'url n'existe pas, alors le message ... apparait. 
3. Si la saisie n'est pas une url, alors le message ... apparait.

Il faut que l'url du site Zalando soit bien celle d'un produit (pour pouvoir analyser les commentaires.

Dans la base de données sont récupérées l'url, la date du jour et le contenu des commentaires sous format xml. 
url et date étant la clé primaire composée, à chaque fois l'utilisateur saisit la même url, le même jour, les éventuels commentaires 
supplémentaires sont ajoutés (update) dans xml (pas de nouvelle ligne créée).

La fiabilité de l'analyse des commentaires dépend de l'exhaustivité des dictionnaires (de mots positifs, négatifs et de la liste poubelle).
