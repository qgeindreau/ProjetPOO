# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 11:34:16 2020

@author: Thomas
"""

nbAuteurs=0
numeroAuteurs=[]

class Auteur:
    
    def __init__(self, nom="", articles=[], citations=[], citePar=[]):
        global nbAuteurs, numeroAuteurs
        self.nom=nom
        self.idArticles=articles
        self.auteursCites=citations
        self.citePar=citePar
        nbAuteurs+=1
        self.numAuteur=nbAuteurs
        numeroAuteurs.append(nbAuteurs)
        
    def setNomAuteur(self,nom=""):
        self.nom=nom
        
        
    def getNbAuteurs(self):
        return nbAuteurs
    
    def __str__(self):
        idArticles=""
        auteursCites=""
        citePar=""
        
        for i in range(len(self.idArticles)-3) : idArticles+= str(self.idArticles[i]) + ", ";
        idArticles+= str(self.idArticles[len(self.idArticles)-2]) + " et " + str(self.idArticles[len(self.idArticles)-1])
        
        for i in range(len(self.auteursCites)-3) : auteursCites+= str(self.auteursCites[i]) + ", ";
        auteursCites+= str(self.auteursCites[len(self.auteursCites)-1]) + " et " + str(self.auteursCites[len(self.auteursCites)-1])
        
        for i in range(len(self.citePar)-3) : citePar+= str(self.citePar[i]) + ", ";
        citePar+= str(self.citePar[len(self.citePar)-2]) + " et " + str(self.citePar[len(self.citePar)-1])
        
        return f"L'auteur {self.nom}, auteur numéro {self.numAuteur},\n\na participé à l'écriture des articles : {idArticles} \n\na cité les auteurs numéro : {auteursCites} \n\net a été cité par les auteurs numéro : {citePar}.\n\n"