#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def reseaux_de_citations(document):#Fonction parcourant le document et renvoyant une liste de tuple (citant, cité) qui nous sert pour générer les graphes
    edges=[]
    with open(document,mode='rb') as f:#On ouvre le document rentré en paramètre en mode 'rb', il me semble qu'il y a moins de chance d'erreurs en mode 'rb'
        for line in f:#on parcours ligne par ligne car la stuture du doc est ainsi: valeur_id_citant valeur_id_cité\n
            ligne = (line.decode(encoding='utf8')).replace('\n','').split(' ')#On récupère la valeur de la ligne, on fais sauter le '\' puis on split avec comme séparateur un espace
            edges.append((ligne[0],ligne[1]))#on ajoute le tuple à la liste
    return edges#On renvoi la liste


if __name__ == "__main__":
    print('Hop hop hop, tu t es perdu ?')