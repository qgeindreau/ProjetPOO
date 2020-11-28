"""
Spyder Editor

This is a temporary script file.
"""

#!/usr/bin/env python
    
import os as os
    

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
    
    
cheminLecture = "hep-th-citations/hep-th-citations"    
#test=getCitations(cheminLecture)
#print(test)

## FAUX : certains identifiants de citant apparaissent 2 fois (ex : 9906064)
def setCitations(pathR,pathW):
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
    citations=getCitations(pathR)
    with open(pathW,"w") as f:
        for citant in citations:
            f.write(str(citant) + " ")
            for cite in citations[citant]:
                f.write(str(cite) + " ")
            f.write("\n")
    return 0           



cheminEcriture = "hep-th-citations/citations-ecriture"
test=setCitations(cheminLecture,cheminEcriture)
#print(test)


"""
def getAuterusArticles(pathR,dossiers,fichiers):
    
    for annee in dossiers:
        for fin_annee in annees:
        with open(path+annee+"/"+fichiers,"r") as f:
"""       


import os
import re

def setAuteurs(pathR,pathW):
    dossiers=os.listdir(cheminLecture)
    listeFichiers=[]
    listeAuteurs=[]
    lignePrecedente=""
    for dossier in dossiers:
        listeFichiers.append(os.listdir(cheminLecture+"/"+str(dossier)))
    n = len(listeFichiers)
    for i in range(n):
            for j in range(len(listeFichiers[i])):
                with open(cheminLecture+"/"+str(dossiers[i])+"/"+str(listeFichiers[i][j]),"r") as f:
                    for ligne in f:
                        ajout=""
                        ajout2=""
                        if str(re.split(" ",lignePrecedente)[0])=="Author:":
                            ajout=listeFichiers[i][j][0:7]+";"+lignePrecedente[8:]
                        if str(re.split(" ",lignePrecedente)[0])=="Authors:":
                            ajout=listeFichiers[i][j][0:7]+";"+lignePrecedente[9:]
                        if (str(re.split(" ",lignePrecedente)[0])=="Author:" or str(re.split(" ",lignePrecedente)[0])=="Authors:") and (str(re.split(" ",ligne)[0])!="Authors:" or str(re.split(" ",ligne)[0])!="Author:"): 
                            if (str(re.split(" ",ligne)[0])!="Comments:" and str(re.split(" ",ligne)[0])!="Journal-ref:" and str(re.split(" ",ligne)[0])!="Subj-class:" and str(re.split(" ",ligne)[0])!="Title"):
                                ajout2=ligne[2:]
                        if ajout!="":
                            listeAuteurs.append(ajout+ajout2)
                        lignePrecedente=str(ligne)
                    #print(cheminLecture+"/"+str(dossiers[i])+"/"+str(listeFichiers[i][j]))
                    print(str(listeFichiers[i][j]),end='')
    with open(pathW,"w") as f:
        for auteur in listeAuteurs:
            f.write(str(auteur) + "\n")
    f=open(pathW,"r")
    remplacementAnd=f.read().replace(" and ",";").replace(", ",";").replace(",",";").replace(" and",";")
    f.close()
    f=open(pathW+"2","w")
    f.write(remplacementAnd)
    f.close()
    return 0


cheminLecture="hep-th-abs"
cheminEcriture="hep-th-abs/auteurs"
test = setAuteurs(cheminLecture, cheminEcriture)
print(test)











