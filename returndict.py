# -*- coding: utf-8 -*-

def returndict(dico):
    newdict={}
    for auteur in dico.keys():
        for i in dico[auteur]:
            try:
                newdict[i].append(auteur)
            except KeyError:
                newdict.update({i:[auteur]})
    return newdict




