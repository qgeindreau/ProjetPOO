# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 10:53:40 2020

@author: Thomas
"""

class Citant():
    
    def __init__(self,citant):
        self.citant = citant
        self.cites=[]
        
    def add_citation(self,cite):
        self.cites.append(cite)
        
    def get_nb_citations(self,citant):
        return len(self.cites)
    
    def get_Id_citant(self):
        return self.citant
    
    def is_cite(self,cite):
        booleen=0
        for cites in self.cites:
            if cite==cites:
                booleen=1
        return booleen
        
    def __str__(self):
        cites=""
        for cite in self.cites:
            cites+=str(cite)+" "
        return f"{self.get_Id_citant()} cite : "+cites
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        