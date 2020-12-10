# -*- coding: utf-8 -*-
import GetDictCit as gdc
import GetDictAuthor as gda
import os
import returndict
import CorrectTheAuthName as ctan
import FuseAndSumDict as fasd

class Communaute:
    def __init__(self,docCitation,pathArticle=os.getcwd()):
        self.dicoCit= gdc.dict_citations(docCitation)
        self.dicoAutArt=gda.Article_Dictionnaire(pathArticle)
        self.dicoArtAut=returndict.returndict(self.dicoAutArt)
        self.dicoCited=returndict.returndict(self.dicoCit)

    def cite(self,name):
        try:
            art_ecrit=self.dicoAutArt[name]
        except KeyError:
            return('Vous voulez peut être dire',ctan.correctName(name),"?")
        art_cite=set()
        for i in art_ecrit:
            try:
                art_cite=art_cite.union(set(self.dicoCit[i]))
            except KeyError:
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

    def influence(self,name,profondeur,_depart=1):
        try:
            list_avant=self.dicoAutArt[name]
        except KeyError:
            return('Vous voulez peut être dire',ctan.correctName(name),"?")
        list_apres=list()
        dico_influence = dict()
        for prof in range(_depart,profondeur+1):
            for art in list_avant:
                try:
                    list_apres+=self.dicoCit[art]
                except KeyError : #Dans le cas ou un article cité n'en cite aucun
                    pass
            for art in set(list_apres):
                try:
                    dico_influence[art]+=list_apres.count(art)/prof
                except KeyError:
                    dico_influence.update({art:(list_apres.count(art))/prof})
            list_avant=list_apres
            list_apres=[]
            dico_influenceAut=dict()
        for art in dico_influence.keys():
            for aut in self.dicoArtAut[art]:
                try:
                    dico_influenceAut[aut]+=dico_influence[art]
                except KeyError :
                    dico_influenceAut.update({aut:dico_influence[art]})
        return dico_influenceAut

    def influenced(self,name,profondeur,_depart=1):
        try:
            list_avant=self.dicoAutArt[name]
        except KeyError:
            return('Vous voulez peut être dire',ctan.correctName(name),"?")
        list_apres=list()
        dico_influence = dict()
        for prof in range(_depart,profondeur+1):
            for art in list_avant:
                try:
                    list_apres+=self.dicoCited[art]
                except KeyError : #Dans le cas ou un article cité n'en cite aucun
                    pass
            for art in set(list_apres):
                try:
                    dico_influence[art]+=list_apres.count(art)/prof
                except KeyError:
                    dico_influence.update({art:(list_apres.count(art))/prof})
            list_avant=list_apres
            list_apres=[]
            dico_influenceAut=dict()
        for art in dico_influence.keys():
            for aut in self.dicoArtAut[art]:
                try:
                    dico_influenceAut[aut]+=dico_influence[art]
                except KeyError :
                    dico_influenceAut.update({aut:dico_influence[art]})
        return dico_influenceAut


    def influenceWCo(self,name,profondeur):
        dic_base=self.influence(name,profondeur)
        for coaut in self.Co_aut(name):
            dic_base= fasd.fas(dic_base,{coaut:1})
            try:
                dic_base=fasd.fas(dic_base,self.influence(coaut, profondeur,2))
            except UnboundLocalError:
                pass
        return dic_base

    def influencedWCo(self,name,profondeur):
        dic_base=self.influenced(name,profondeur)
        for coaut in self.Co_aut(name):
            dic_base= fasd.fas(dic_base,{coaut:1})
            try:
                dic_base=fasd.fas(dic_base,self.influenced(coaut, profondeur,2))
            except UnboundLocalError:
                pass
        return dic_base

    def communaute(self,name,profondeur):
        return set((self.influence(name,profondeur)).keys()).intersection(set((self.influenced(name, profondeur)).keys()))




