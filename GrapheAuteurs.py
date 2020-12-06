# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 10:51:13 2020

@author: Thomas
"""

import networkx as nx

def getCitations(path):
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
        citations={}
        a=[]
        for ligne in f:
            citant = ligne.split()[0] #Id article citant
            cite = ligne.split()[1] #Id article cité
            a.append(ligne.split()[0])
            if citant in citations:
                citations[citant].append(cite)
            else:
                citations[citant] = [cite]
    return citations
    



def setCitations(pathR):
    """

    Parameters
    ----------
    pathR : String
        Chemin du fichier à lire.
    pathW : String
        Chemin du fichier dans lequel écrire.

    Returns
    -------
    None.

    """
    grapheCitations = nx.DiGraph()
    dicoCitations=getCitations(pathR)
    for citant in dicoCitations:
        grapheCitations.add_node(citant)
        for cite in dicoCitations[citant]:
            grapheCitations.add_edge(citant, cite, weight=1)
    return grapheCitations,dicoCitations




def getInfluenceursAAvecProf(graphe,dico,A,N):
    influenceurs={}
    for i in range(N+1):
        influenceurs[i]=[]
    return recursif(graphe,dico,A,N,0,influenceurs)

def recursif(graphe,dico,A,N,n,influenceurs):
    if A not in dico:
        return
    if n==N:
        for influenceur in dico[A]:
            influenceurs[n].append(influenceur)
        return 
    for influenceur in dico[A]:
        influenceurs[n].append(influenceur)
    for inf in dico[A]:
        recursif(graphe,dico,inf,N,n+1,influenceurs)
    
    return influenceurs

def getInfluenceursA(graphe,dico,A,N):
    if A not in dico:
        return []
    dicoInfluenceurs=getInfluenceursAAvecProf(graphe,dico,A,N)
    result=[]
    for i in range(len(dicoInfluenceurs)):
        for inf in dicoInfluenceurs[i]:
            result.append(inf)
    return list(set(result)) #list(set()) enleve tous les doublons
        
def getCommunauteA(graphe,dico,A,N):
    influenceursA=getInfluenceursA(graphe,dico,A,N)
    communaute=[]
    print(f"influenceursA : {influenceursA}")
    for influenceur in influenceursA:
        if A in getInfluenceursA(graphe,dico,influenceur,N):
            communaute.append(influenceur)
    return communaute


import Configuration as cf

cheminLecture = cf.getChemin("lecture")
  
graphe,dico=setCitations(cheminLecture)

#print(getInfluenceursAAvecProf(graphe, dico, "0001003", 2))

#print(getInfluenceursA(graphe, dico, "0001003", 2))
#print(getInfluenceursA(graphe, dico, "0001004", 2))

#print(getCommunauteA(graphe, dico, "0001003", 2))


"""
cheminLecture = "hep-th-citations/hep-th-citations-mini"  
graphe,dico=setCitations(cheminLecture)
nx.draw(graphe,pos=nx.circular_layout(graphe),with_labels=True)
"""

from Auteur import Auteur 

test = Auteur("Test1",dico["0001001"], [1,2,3,4,7,8,9], [9,8,7,4,1,0])
print(test)
test2 = Auteur("Test2",dico["0001001"], [1,2,3,4,7,8,9], [9,8,7,4,1,0])
test3 = Auteur("Test3",[1856,81,6,18,41,635,16,81,6,7], [1,2,3,4,7,8,9], [9,8,7,4,1,0])
print(test3)




























