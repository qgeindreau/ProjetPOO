# -*- coding: utf-8 -*-
import chardet

def dict_citations(document):
    List_Article=[]
    dico={}
    with open(document, mode='rb') as f :
        comparateur= str
        for line in f:
            encod=chardet.detect(line)['encoding']
            base=line.split(bytes(" ", encoding=encod))[0]
            reference=line.split(bytes(" ", encoding=encod))[1]
            if comparateur!=base:
                List_Article=[]
            List_Article.append(reference.replace(bytes('\n',encoding=encod),bytes('',encoding=encod)).decode())
            dico[base.decode()]=List_Article
            comparateur=base
    return dico

open('dictionnaire citation','wb').write(bytes(str(dict_citations('hep-th-citations')),encoding='ASCII'))