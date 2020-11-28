# -*- coding: utf-8 -*-
import os
import re
import CorrectTheAuthName as ca
#Warner nous oblige à ne prendre que les initiales des prénoms
def make_bad_char_boom(text):
    usefultext="azertyuiopqsdfghjklmwxcvbn.,&AZERTYUIOPQSDFGHJKLMWXCVBN"
    corrected=''
    for i in range(len(text)):
        if usefultext.find(text[i])!=(-1):
            corrected+=text[i]
    return corrected

def add_space_before_maj(text):
    usefultext="AZERTYUIOPQSDFGHJKLMWXCVBN"
    newnam=''
    for i in range(len(text)):
        if usefultext.find(text[i])!=(-1):
            newnam+=' '
        newnam+=text[i]
    return(newnam[1:])


def Article_Dictionnaire(y_b=1992,y_e=2003):
    dictionnaire={}
    main_dir=os.getcwd()

    list_dossier = [str(i) for i in range(y_b,y_e+1)]
    for ss_dos in list_dossier :
        os.chdir(ss_dos)
        for fichier in os.listdir():

            with open(fichier, 'rb') as f:
                find = False
                for line in f:
                    if line.decode().find('Author')==(0) and (find == False):
                        Auteurs=line.decode()[8:]
                        find = True
                    elif (find == True) and line.decode('utf-8').find(' ')==(0):
                        Auteurs+=line.decode()[1:]
                    elif (find == True) and line.decode('utf-8').find(' ')!=(0):
                        Auteurs=Auteurs.replace('\n','' )
                        Auteurs=re.sub(r'\(.*\)', '', Auteurs)
                        Auteurs=Auteurs.replace(' and ',',')
                        Auteurs=Auteurs.replace(' ','')
                        Auteurs=Auteurs.replace(',,','')
                        Auteurs=make_bad_char_boom(Auteurs)
                        if Auteurs[len(Auteurs)-1]==',':
                            Auteurs=Auteurs[:(len(Auteurs)-1)]
                        try:
                            dictionnaire.update({fichier.replace('.abs','') : ca.correctName(re.split(',|&',add_space_before_maj(Auteurs)))})
                        except IndexError:
                            print(fichier,' non pris en compte car non conforme')
                        break

        os.chdir(main_dir)
    return dictionnaire

open('Articles_Auteurs','wb').write(bytes(str(Article_Dictionnaire()),encoding='utf-8'))