#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def fas(dico1,dico2):#Fonction prenant deux dictionnaire, en créant un unique avec les clés des deux et les valeurs additionnées
    for key in dico2.keys():
        try: #On cherche la clé si elle n'exite pas, on la crée
            dico1[key]+=dico2[key]
        except KeyError :
            dico1.update({key:dico2[key]})
    return dico1
