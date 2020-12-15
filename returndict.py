#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def returndict(dico):#Fonction permettant d inverser un dico avec des listes en valeurs: exemple {'chat':['4pattes','familier],'sanglier':['4pattes','sauvage']} devient
    #{'4pattes':['chat','sanglier'],'familier':['chat'],'sauvage':['sanglier']}
    newdict={}
    for auteur in dico.keys():
        for i in dico[auteur]:
            try:
                newdict[i].append(auteur)
            except KeyError:
                newdict.update({i:[auteur]})
    return newdict




