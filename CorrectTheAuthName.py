#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests#Module pour gérer les requetes
import json#Module pour gérer les fichier.json
def correctName(nom):#Fonction pour corriger un nom d'auteur présant dans la bdd du site hep-inspire
    if type (nom)==(str):#On vérifie que le type de la variable d'entrée est une chaîne dde caractères
        nom.replace('Jr.','')#On supprime le Jr., après de multiple test, il est à l'origine de moultes erreurs
        try:#On essai de récupérer le nom de la personne entrée en tant que dernière partie( Prénom+' '+nom)
            ndf=nom.split(' ')
            ndf=ndf[len(ndf)-1]
        except :#En cas d'erreur(chaîne vide principalement)
            print('Nom non valide')
            return(nom) #On renvoie quand même le nom de base
        url="https://inspirehep.net/api/authors?sort=bestmatch&size=25&page=1&q="+nom.replace(' ','%20')#Url de l'api qui nous sert pour corriger le nom de l'auteur 
        #(il est spécifié dans leur Git qu il faut remplacer les espaces par des %20)
        response= requests.get(url) #On fais la requete (On devrait rajouté que la reponse vaut bien 200)
        raw_data=response.text#raw_data correspond au code source sans les balises html
        jsondata=json.loads(raw_data)#On charge les information comme un json (C est ce que nous renvoi l'api, un json avec toutes les infos de la page)
        for i in range(5):#On ne prends que les 5 premiers résultat de la recherche, afin d'éviter que le programme ne tourne trop longtemps, même si,
            #étant donnée que l'on quitte la boucle si un nom nous convient en soit, ça ne change pas grand chose
            try:#sécurité +/- inutiles, au cas ou un cas de figure inconnue nous arrives
                if jsondata['hits']['hits'][i]['metadata']['name']['preferred_name'].find(ndf)!=(-1) and jsondata['hits']['hits'][i]['metadata']['name']['preferred_name'][0]==nom.replace(' ','')[0]:
                    #On prend comme critère le nom de famille et la première lettre du prénom
                    return(jsondata['hits']['hits'][i]['metadata']['name']['preferred_name'])#Le cas échéant, on renvoie la version corrigée (quelques erreurs subsiste en cas d'homonyme avec des prénom commencant pareil)
            except IndexError:
                print('Nom non valide')
                return(nom)
        return(nom)#Si on ne trouve pas de correction intéressante, on préfére ne rien changer
    if type(nom)==(list):#Si le nom entré est une liste, on applique la fonction à chacun de ses termes
        for i in range(len(nom)):
                nom[i]=correctName(nom[i])
        return nom

