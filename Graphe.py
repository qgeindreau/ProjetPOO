# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 15:05:04 2020

@author: Thomas
"""

import networkx as nx
from itertools import chain

"""
G = nx.DiGraph()

G.add_node(1)
G.add_nodes_from([2,3])
G.add_edge(4, 2)
G.add_edge(2, 3)
G.add_edge(3, 5, weight=6)
G.add_edge(4, 5, weight=6)
G.add_edge(2, 5)
G.add_edge(5, 1)
print(G)

nx.draw(G,pos=nx.circular_layout(G),with_labels=True)

print(G)

print(nx.dijkstra_path(G,4,5))
print(len(nx.dijkstra_path(G,4,5)))
print(nx.edges(G,5))
"""
    

def countDegre(graphe,noeud):
    degrePositif=0
    degreNegatif=0
    listeVoisins = nx.all_neighbors(graphe,noeud)
    for voisin in listeVoisins:
        if (voisin,noeud) in nx.edges(graphe,voisin):
            degreNegatif+=1
        elif (noeud,voisin) in nx.edges(graphe,noeud):
            degrePositif+=1
    return [degrePositif,degreNegatif]

def getGrapheCitations(path):
    """

    Parameters
    ----------
    path : String
        Chemin du fichier à lire.

    Returns
    -------
    citations : Dictionnaire
        Dictionnaire ayant en indexs les citants et en valeurs associées les cités par le citant.

    """
    with open(path,"r") as f:
        graphe=nx.DiGraph()
        for ligne in f:
            citant = ligne.split()[0] #Id article citant
            cite = ligne.split()[1] #Id article cité
            graphe.add_edge(citant,cite, weight=1)
    return graphe
   
""" 
def cheminsCitationsLongueur(graphe,depart,N):
    noeudLongueur=[]
    for node in sorted(graphe):
        print("I",end='')
        if node==depart:
            pass
        try:
            if len(nx.dijkstra_path(graphe,depart,node))<=N:
                noeudLongueur.append(node)
                noeudLongueur.append(len(nx.dijkstra_path(graphe,depart,node)))
        except:
            pass
    return noeudLongueur
"""
def cheminsCitationsLongueur(graphe,depart,N):
    tabCites={}
    tabCites[0]=depart
    n=0
    tabEtudies=nx.neighbors(graphe,depart)
    while n<N:
        n+=1
        tabCites[n]=[]
        for cite in tabEtudies:
            tabCites[n].append(cite)
        for i in range(len(tabCites[n])):
            for mot in nx.neighbors(graphe,int(tabCites[n][i])):
                print("a ",mot)
            pass
    return tabCites
        
    


cheminLecture = "hep-th-citations/hep-th-citations"
graphe = getGrapheCitations(cheminLecture)
print(countDegre(graphe,"0001001"))

test = cheminsCitationsLongueur(graphe, "0001001", 3)
print(test)


cheminLecture = "hep-th-citations/hep-th-citations-mini"
graphe = getGrapheCitations(cheminLecture)
print(cheminsCitationsLongueur(graphe,"0001001", 3))
print("dessin...")
#nx.draw(test,pos=nx.circular_layout(test),with_labels=True)
print("fini")





cheminLecture = "hep-th-citations/hep-th-citations-mini"
graphe = getGrapheCitations(cheminLecture)
nx.draw(graphe,pos=nx.circular_layout(graphe),with_labels=True)
depart="0001001"
print(cheminsCitationsLongueur(graphe, depart, 3))















































