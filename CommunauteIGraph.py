#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import GetGraphAut as gga
import GetEdgesCit as gig
from IgraphTo3d import Modelize
import FuseAndSumDict as fasd
import networkx as nw
import igraph as ig
import os
import CorrectTheAuthName as ctan
import pickle
import itertools

class CommunauteIGraph:
    def __init__(self,doc_citations,path_Article=os.getcwd(),corrected='N',Traduit='N'):
        Aut = gga.GraphAut(path=path_Article,corrected=corrected,Traduit=Traduit)#Variable enregistrant toutes les infos
        self.VisualGraph=Aut[0]#Graph  igraph qui va servir pour la modélisation 3D
        self.dicoAutArt=Aut[1]#Dico: {Auteur:[Articles]}
        self.dicoArtAut=Aut[2]#Dico:{Article:[Auteurs]}
        self.edges = gig.reseaux_de_citations(doc_citations)#Liste de tuple des citations
        self.VisualGraph.add_edges(self.edges)#On ajoute les citations comme lien dans le igraph
        self.NwGraph=nw.DiGraph(self.edges)#Graph Networkx qui va servir à faire les différents calculs d'influence et les méthodes
        self.NwGraph.add_nodes_from(self.dicoArtAut.keys())#On ajoutes les nodes de tous les Articles, si ils y sont déja, ca ne change rien

    def cite(self,name,Vision3D=False):
        '''
        

        Parameters
        ----------
        name : Nom de l'auteur

        Returns
        -------
        Renvoi la liste des auteurs cité par celui en paramètre

        '''
        try:
            art_ecrit=self.dicoAutArt[name]#On prend la liste des articles écrit par l'auteur dont le nom est rentré en paramètre
        except KeyError:#En cas de KeyError, l'auteur n'existe pas dans le dictionnaire, on propose alors une version corrigé du nom
            return 'Vous voulez peut être dire '+ctan.correctName(gga.add_space_before_maj(name))+" ?"
        art_cite=set()#On créer un ensemble vide dans lequel on va ajouter les article cité par les article de name
        for i in art_ecrit:#On parcours les articles écrit par name
            try:#Non necessaire, uniquement présent car sait-on jamais, il peut y avoir des pièges ou
            #un article qui en cite un qui n est pas dans notre base de données de citation
                art_cite=art_cite.union(set(self.NwGraph.successors(i)))#On ajoute aux articles cités ceux cité par l'article i
            except :
                pass
        aut_cit=set()#Future ensemble des auteurs cités
        for i in art_cite:#On parcours les articles cités
            try:#Si un article est cité mais ne fait pas parti de notre base de données d'abstracts.
                aut_cit=aut_cit.union(set(self.dicoArtAut[i]))#On ajoutes les auteurs de l article cité i
            except KeyError:
                pass
        if Vision3D!='n' and Vision3D !='N':
            sub_graph=self.VisualGraph.subgraph(list(aut_cit)+list(art_cite)+[name]+art_ecrit)
            titre='Modelisation 3D des citations de <br>'+name
            position=sub_graph.vs['name'].index(name)
            sub_graph.vs[position]['symbole'],sub_graph.vs[position]['Taille']='circle',20
            Modelize(sub_graph,titre=titre)
        return(aut_cit)

    def Co_aut(self,name):
        try:#Comme pour au dessus, si l auteur n est pas dans notre bdd, on propose une version corrigé de son nom
            art_ecrit=self.dicoAutArt[name]
        except KeyError:
            return 'Vous voulez peut être dire '+ ctan.correctName(name)+'?'
        co_aut=set()#Ensemble des coauteurs
        for i in art_ecrit:#On parcours les articles écrit par name
            try:#On passe en try par pure sécurité, en théorie, si l'article à été écrit par name, il dispose d'au moins un auteur
                co_aut=co_aut.union(set(self.dicoArtAut[i]))
            except KeyError :
                print(i,'pose problème')
            co_aut.discard(name)#On retire name de la liste de ses coauteurs
            return co_aut



    def influenceArt(self,art,profondeur=1):
        i=0
        mat_influence=nw.to_pandas_adjacency(nw.ego_graph(self.NwGraph, art, radius=profondeur))#On prends la matrice d'adjacence du graphe réduit
        #Cela permet de simplifier les calculs pour l'ordinateur
        mat_bis =mat_influence.copy()#On définie mat bis qui va monter en puissance
        mat_prod=mat_influence.copy()#Mat_prod vas nous servir à faire monter mat bis en puissance
        for i in range(2,profondeur+1): #On va de 2 à profondeur plus 1, comme ça on a pas besoin de faire i+1 pour calculer l intensité
        #d'influence
            mat_bis=mat_bis.dot(mat_prod)#On fait monter mat_bis en puissance à chaque itération
            mat_influence += (mat_bis/i)#Car l intensité d'influence ce mesure par +nb d appel/distance d appel
        dico=dict(mat_influence.loc[art])#On rend la ligne qui correspond à l influence de l'article souhaité sous forme de dictionnaire
        return dico

    def influence(self,name,profondeur=1):
        try:#Comme d'habitude, si name n est pas dans notre bdd d auteurs, on propose une correction
            art_ecrit=self.dicoAutArt[name]#Liste des articles écrits par name
        except KeyError:
            return 'Vous voulez peut être dire '+ctan.correctName(name)+"?"
        dico_influence={}#On créer un dico vide qui vas accueillir les articles influencant
        for art in art_ecrit:
            dico_influence=fasd.fas(dico_influence,self.influenceArt(art,profondeur))#On ajoutes au dictionnaire les nouveaux
            #article d'influence et leur influence et on augmente l influence de ceux déjà influençant.
        new_dict={}#dico qui va accueillir les auteurs d'influence
        for art in dico_influence.keys():
            for aut in self.dicoArtAut[art]:
                new_dict=fasd.fas(new_dict,{aut:dico_influence[art]})
        return new_dict

    def influencedArt(self,art,profondeur=1):#Comme pour InfluenceArt mais en prenant de graphe avec les arc retournés
        mat_influence=nw.to_pandas_adjacency(nw.ego_graph(self.NwGraph.reverse(), art, radius=profondeur))
        mat_bis =mat_influence.copy()
        mat_prod=mat_influence.copy()
        for i in range(2,profondeur+1):
            mat_bis=mat_bis.dot(mat_prod)
            mat_influence += (mat_bis/i)
        dico=dict(mat_influence.loc[art])
        return dico

    def influenced(self,name,profondeur=1):#Comme pour influence mais avec influencedArt

        try:
            art_ecrit=self.dicoAutArt[name]
        except KeyError:
            return  'Vous voulez peut être dire '+ ctan.correctName(name)+'?' 
        dico_influence={}
        for art in art_ecrit:
            dico_influence=fasd.fas(dico_influence,self.influencedArt(art,profondeur))
        new_dict={}
        for art in dico_influence.keys():
            for aut in self.dicoArtAut[art]:
                new_dict=fasd.fas(new_dict,{aut:dico_influence[art]})
        return new_dict

    def communaute(self,name,profondeur=1):#On définie la communauté comme l'intersection de ceux qui influence et ceux qui sont influencé
        return set((self.influence(name,profondeur)).keys()).intersection(set((self.influenced(name, profondeur)).keys()))


    def chemin_le_plus_rapide(self,name1,name2):
        try:
            tr_graph=self.VisualGraph
            list_utile=[i for i in range(tr_graph.vcount()-1) if (tr_graph.vs[i]['genre']=='Article' or tr_graph.vs[i]['name']==name1 or tr_graph.vs[i]['name']==name2 )]
            tr_graph=tr_graph.subgraph(list_utile)
            chemin=tr_graph.get_all_shortest_paths(name1,name2)
            point_utile=list(itertools.chain(*chemin))
            tr_graph=tr_graph.subgraph(point_utile)
            Modelize(tr_graph,titre=' Chemins de citations les plus court de '+name1 +'<br> Vers '+name2)
        except ValueError:
            return 'Vous voulez dire: '+ctan.correctName(name1)+' et '+ ctan.correctName(name2)+' ?'
        return
