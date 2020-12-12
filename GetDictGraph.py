# -*- coding: utf-8 -*-
import networkx as nw

def reseaux_de_citations(document):
    graphe_cit = nw.DiGraph()
    with open(document,mode='rb') as f:
        for line in f:
            ligne = (line.decode(encoding='utf8')).replace('\n','').split(' ')
            graphe_cit.add_edge(ligne[0], ligne[1],weight=1)
    return graphe_cit

