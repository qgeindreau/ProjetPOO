#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import CorrectTheAuthName as ca
import concurrent.futures
from textblob import TextBlob
import igraph as ig
import returndict as rd

def corname(name):
    return [name,ca.correctName(add_space_before_maj(name))]

def CorrectDico(dictionnaire):
    dico={}
    with concurrent.futures.ThreadPoolExecutor() as executor:
        aut=executor.map(corname, dictionnaire.keys())
        aut=list(aut)
        for i in range(len(aut)):
            try:
                dico[aut[i][1]]+=dictionnaire[aut[i][0]]
            except KeyError:
                dico.update({aut[i][1]:dictionnaire[aut[i][0]]})
    return(dico)
def tratext(text,langue='fr'):
    return [text,Traduct(text,langue)]


def Traduct(text,langue='fr'):
    blob = TextBlob(text)
    try:
        return(str(blob.translate(to=langue)))
    except :
        return text


def TradDico(dico,langue='fr'):
    dico2={}
    with concurrent.futures.ThreadPoolExecutor() as executor:
        aut=executor.map(tratext, dico.keys(),[langue for i in range(len(dico.keys()))])
        aut=list(aut)
        for i in range(len(aut)):
            try:
                dico2[aut[i][1]]+=dico[aut[i][0]]
            except KeyError:
                dico2.update({aut[i][1]:dico[aut[i][0]]})
    return dico2


def add_space_before_maj(text):
    usefultext="AZERTYUIOPQSDFGHJKLMWXCVBN"
    newnam=''
    for i in range(len(text)):
        if usefultext.find(text[i])!=(-1):
            newnam+=' '
        newnam+=text[i]
    return(newnam[1:])

def make_bad_char_boom(text):
    usefultext="azertyuiopqsdfghjklmwxcvbn.,&AZERTYUIOPQSDFGHJKLMWXCVBN"
    corrected=''
    for i in range(len(text)):
        if usefultext.find(text[i])!=(-1):
            corrected+=text[i]
    return corrected


def GraphAut(path=os.getcwd(),corrected='n',Traduit='n'):
    dictionnaire={}
    main_dir=os.getcwd()
    os.chdir(path)
    new_dir=os.getcwd()
    dico_titre={}
    list_dossier = list(filter(os.path.isdir, os.listdir(os.curdir)))
    try:
        list_dossier.remove('__pycache__')
    except ValueError:
        pass
    for ss_dos in list_dossier :
        os.chdir(ss_dos)
        list_fichier=os.listdir()
        for fichier in list_fichier:
            if fichier.find('.abs')==(-1):
                list_fichier.remove(fichier)
        for fichier in list_fichier:

            with open(fichier, 'rb') as f:
                find = False
                trileen_titre=0
                for line in f:
                    if trileen_titre==0 and line.decode('utf-8').find('Title')==0:
                        titre=line.decode()[6:]
                        trileen_titre+=1
                    elif trileen_titre==1 and line.decode('utf-8').find(' ')==0:
                        titre+= line.decode()[1:]
                    elif trileen_titre==1 and line.decode('utf-8').find(' ')!=0:
                        trileen_titre+=1
                        dico_titre.update({fichier.replace('.abs',''):titre.replace('\n','')})
                    if line.decode().find('Author')==(0) and (find == False):
                        Auteurs=line.decode()[8:]
                        find = True
                    elif (find == True) and line.decode('utf-8').find(' ')==(0):
                        Auteurs+=line.decode()[1:]
                    elif (find == True) and line.decode('utf-8').find(' ')!=(0):
                        Auteurs= Auteurs.replace('\n','' )
                        Auteurs=re.sub(r'\(.*\)', '', Auteurs)
                        Auteurs=Auteurs.replace(' and ',',')
                        Auteurs=Auteurs.replace(' ','')
                        Auteurs=Auteurs.replace(',,',',')
                        Auteurs=make_bad_char_boom(Auteurs)
                        if Auteurs[len(Auteurs)-1]==',':
                            Auteurs=Auteurs[:(len(Auteurs)-1)]
                        Auteurs=re.split(',|&',Auteurs)
                        if trileen_titre==0 and line.decode('utf-8').find('Title')==0:
                            dico_titre.update({fichier.replace('.abs',''):titre.replace('\n','')})
                        for aut in Auteurs:
                                try:
                                    dictionnaire[aut].append(fichier.replace('.abs', ''))
                                except KeyError:
                                    dictionnaire.update({aut:[fichier.replace('.abs', '')]})
                        break

        os.chdir(new_dir)
    os.chdir(main_dir)
    if corrected!='n' and corrected!='N':
        dictionnaire=CorrectDico(dictionnaire)
    if Traduit!='n' and Traduit != 'N':
        dico_titre=TradDico(dico_titre,Traduit)
    MonBeauGraph=ig.Graph(directed=True)
    edges=list()
    i=0
    for key in dictionnaire.keys():
        MonBeauGraph.add_vertices(key)
        MonBeauGraph.vs[i]['genre']='Auteur'
        MonBeauGraph.vs[i]['label']=str(MonBeauGraph.vs[i]['name'])
        MonBeauGraph.vs[i]['group']=1
        MonBeauGraph.vs[i]['symbole']='diamond'
        MonBeauGraph.vs[i]['Taille']=10
        i+=1
        for article in dictionnaire[key]:
            edges.append((key,article))
            edges.append((article,key))
    for key in rd.returndict(dictionnaire).keys():
        MonBeauGraph.add_vertices(key)
        MonBeauGraph.vs[i]['genre']='Article'
        MonBeauGraph.vs[i]['group']=(int(key[1])+2)
        MonBeauGraph.vs[i]['symbole']='square'
        MonBeauGraph.vs[i]['Taille']=5
        try:
            MonBeauGraph.vs[i]['label']=str(dico_titre[key])
        except KeyError:
            MonBeauGraph.vs[i]['label']=str(MonBeauGraph.vs[i]['name'])
        i+=1
    MonBeauGraph.add_edges(edges)
    return [MonBeauGraph,dictionnaire,rd.returndict(dictionnaire)]
