# -*- coding: utf-8 -*-

import GetDictGraph as gdg
import GetDictAuthor as gda
import os
import returndict
import networkx as nw
import CorrectTheAuthName as ctan
import FuseAndSumDict as fasd
import time
import concurrent.futures
class CommunauteWGraph:
    def __init__(self,docCitation,pathArticle=os.getcwd()):
        self.GraphCit= gdg.reseaux_de_citations(docCitation)
        self.dicoAutArt=gda.Article_Dictionnaire(pathArticle)
        self.dicoArtAut=returndict.returndict(self.dicoAutArt)
        for art in self.dicoArtAut.keys():
            self.GraphCit.add_node(art)

    def cite(self,name):
        try:
            art_ecrit=self.dicoAutArt[name]
        except KeyError:
            return 'Vous voulez peut être dire '+ctan.correctName(name)+" ?"
        art_cite=set()
        for i in art_ecrit:
            try:
                art_cite=art_cite.union(set(self.GraphCit.successors(i)))
            except nw.NetworkXError:
                pass
        aut_cit=set()
        for i in art_cite:
            try:
                aut_cit=aut_cit.union(set(self.dicoArtAut[i]))
            except KeyError:
                pass
        return(aut_cit)

    def Co_aut(self,name):
        try:
            art_ecrit=self.dicoAutArt[name]
        except KeyError:
            return('Vous voulez peut être dire',ctan.correctName(name),'?')
        co_aut=set()
        for i in art_ecrit:
            try:
                co_aut=co_aut.union(set(self.dicoArtAut[i]))
            except KeyError :
                pass
            co_aut.discard(name)
            return co_aut

    def influenceArt(self,art,profondeur):
        mat_influence=nw.to_pandas_adjacency(nw.ego_graph(self.GraphCit, art, radius=profondeur))
        mat_bis =mat_influence.copy()
        mat_prod=mat_influence.copy()
        for i in range(2,profondeur+1):
            mat_bis=mat_bis.dot(mat_prod)
            mat_influence += (mat_bis/i)
        dico=dict(mat_influence.loc[art])
        return dico

    def influence(self,name,profondeur):
        '''
        

        Parameters
        ----------
        name : TYPE
            DESCRIPTION.
        profondeur : TYPE
            DESCRIPTION.

        Returns
        -------
        new_dict : TYPE
            DESCRIPTION.

        '''
        try:
            art_ecrit=self.dicoAutArt[name]
        except KeyError:
            return('Vous voulez peut être dire',ctan.correctName(name),"?")
        dico_influence={}
        for art in art_ecrit:
            dico_influence=fasd.fas(dico_influence,self.influenceArt(art,profondeur))
        new_dict={}
        for art in dico_influence.keys():
            for aut in self.dicoArtAut[art]:
                new_dict=fasd.fas(new_dict,{aut:dico_influence[art]})
        return new_dict

    def influencedArt(self,art,profondeur):
        mat_influence=nw.to_pandas_adjacency(nw.ego_graph(self.GraphCit.reverse(), art, radius=profondeur))
        mat_bis =mat_influence.copy()
        mat_prod=mat_influence.copy()
        for i in range(2,profondeur+1):
            mat_bis=mat_bis.dot(mat_prod)
            mat_influence += (mat_bis/i)
        dico=dict(mat_influence.loc[art])
        return dico

    def influenced(self,name,profondeur):
        '''
        

        Parameters
        ----------
        name : TYPE
            DESCRIPTION.
        profondeur : TYPE
            DESCRIPTION.

        Returns
        -------
        new_dict : TYPE
            DESCRIPTION.

        '''
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

    def communaute(self,name,profondeur):
        return set((self.influence(name,profondeur)).keys()).intersection(set((self.influenced(name, profondeur)).keys()))

