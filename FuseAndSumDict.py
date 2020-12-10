# -*- coding: utf-8 -*-

def fas(dico1,dico2):
    new_dict=dict()
    for key in dico1.keys():
        new_dict.update({key:dico1[key]})
    for key in dico2.keys():
        try:
            new_dict[key]+=dico2[key]
        except KeyError :
            new_dict.update({key:dico2[key]})
    return new_dict

