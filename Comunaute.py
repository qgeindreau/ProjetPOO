#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from GetFichier import get_files 
import CommunauteIGraph as cig
import pickle
import sys
import json
import os


if __name__ == "__main__":
    commande=sys.argv
    continuer=True
    config=json.load(open('config.json','rb'))
    print(config)
    try:
        commu_I_Graph= pickle.load(open('savecommu.p','rb'))
        initialise=True
    except:
        initialise=False
        pass

    while continuer:
        try:
            if len(commande)==1 or commande[1]==("Help" and "help"):
                print("\nVoici la liste des arguments à passer en paramètre suite à l'appel du script :\n\n\
get_fichiers [url_citations url_abstracts] première chose à faire pour un nouvel ensemble de données \n\
init references.txt [articles.d] \n\
cite Auteur [vision] \n\
influence Auteur Profondeur_D'influence [vision] \n\
influenced Auteur Profondeur_D'influence [vision] \n\
communaute Auteur Profondeur [vision] \n\
co-auteur Auteur [vision]\n\
chemin Auteur1 Auteur2" )

                
            elif commande[1]==("Get_fichiers" and "get_fichiers"):
                try:
                    if len(commande)==2:
                        get_files(config['link_abstracts'],config['link_citations'])
                    elif len(commande)>2:
                        get_files(commande[2],commande[3])
                    print("Les fichiers sont importés.")
                except:
                    raise Exception
                
                
            elif commande[1]==("Init" and "init"):
                if len(commande)==2:
                    try:
                        commu_I_Graph = cig.CommunauteIGraph(os.getcwd()+"/hep-th-citations",corrected=config['Corrige'])
                        pickle.dump(commu_I_Graph,open('savecommu.p','wb'))
                    except KeyError:
                        print('Commande mal rentrée \nExecutez sans paramètres pour plus de détails')
                elif len(commande)==3:
                    try:
                        commu_I_Graph = cig.CommunauteIGraph(commande[2],corrected=config['Corrige'])
                        pickle.dump(commu_I_Graph,open('savecommu.p','wb'))
                    except KeyError:
                        print('Commande mal rentrée \nExecutez sans paramètres pour plus de détails')
                else:
                    try:
                        commu_I_Graph = cig.CommunauteIGraph(commande[2],commande[3],corrected=config['Corrige'])
                        pickle.dump(commu_I_Graph,open('savecommu.p','wb'))
                    except:
                        print('Commande mal rentrée \nExecutez sans paramètres pour plus de détails')
                initialise=True
                print("L'initialisation est finie.")
                        
            elif initialise==False:
                print("\nFaites un init d'abord")
                raise Exception
                
                
            elif commande[1]==("Cite" and "cite"):
                print('Dans la boucle')
                if len(commande)==2:
                    print("Pour rappel, les paramètres de cite : le nom d'un Auteur\n")
                    raise Exception
                try:
                    citee = commu_I_Graph.cite(commande[2],Vision3D=config['Vision3D'])
                    print(citee)
                except KeyError:
                    print('Commande mal rentrée \nExecutez sans paramètres pour plus de détails')
                
                    
            
            elif commande[1]==("Influence" and "influence"):
                if len(commande)==2:
                    print("Pour rappel, les paramètres de influence : un nom d'Auteur [, une profondeur]\n")
                    raise Exception
                elif len(commande)==3:
                    try:
                        influence = commu_I_Graph.influence(commande[2])
                        print(influence)
                    except KeyError:
                        print('Commande mal rentrée \nExecutez sans paramètres pour plus de détails')
                else:
                    try:
                        influence = commu_I_Graph.influence(commande[2],commande[3])
                        print(influence)
                    except:
                        print('Commande mal rentrée \nExecutez sans paramètres pour plus de détails')
                        
                
            elif commande[1]==("Influenced" and "influenced"):
                if len(commande)==2:
                    print("Pour rappel, les paramètres de influenced : un nom d'Auteur [, une profondeur]\n")
                    raise Exception
                elif len(commande)==3:
                    try:
                        influenced = commu_I_Graph.influenced(commande[2])
                        print(influenced)
                    except KeyError:
                        print('Commande mal rentrée \nExecutez sans paramètres pour plus de détails')
                else:
                    try:
                        influenced = commu_I_Graph.influenced(commande[2],commande[3])
                        print(influenced)
                    except:
                        print('Commande mal rentrée \nExecutez sans paramètres pour plus de détails')
                        
                        
            elif commande[1]==("Communaute" and "communaute"):
                print(1)
                if len(commande)==2:
                    print("Pour rappel, les paramètres de communaute : un nom d'Auteur [, une profondeur]\n")
                    raise Exception
                elif len(commande)==3:
                    print(2)
                    try:
                        print(3)
                        commu = commu_I_Graph.communaute(str(commande[2]))
                        print(4)
                        print(commu)
                    except KeyError:
                        print('Commande mal rentrée \nExecutez sans paramètres pour plus de détails')
                else:
                    print(5)
                    try:
                        print(6)
                        commu = commu_I_Graph.communaute(commande[2],commande[3])
                        print(commu)
                    except:
                        print('Commande mal rentrée \nExecutez sans paramètres pour plus de détails')
                print(7)
                        
                        
                        
            elif commande[1]==("Co-auteur" and "co-auteur"):
                if len(commande)==2:
                    print("Pour rappel, les paramètres de co-auteur : un nom d'Auteur\n")
                    raise Exception
                else:
                    try:
                        coaut = commu_I_Graph.co_aut(commande[2])
                        print(coaut)
                    except KeyError:
                        print('Commande mal rentrée \nExecutez sans paramètres pour plus de détails')

            elif commande[1]==('Chemin' and 'chemin'):
                try:
                    commu_I_Graph.chemin_le_plus_rapide(commande[2],commande[3])
                except:
                    raise Exception
            
            else:
                raise Exception
            
            
        except:
            print("\nVous n'avez pas rentré une commande valide, \n\
voici la liste des arguments à passer en paramètre suite à l'appel du script :\n\n\
get_fichiers [url_citations url_abstracts] première chose à faire pour un nouvel ensemble de données \n\
init references.txt [articles.d] \n\
cite Auteur [vision] \n\
influence Auteur Profondeur_D'influence [vision] \n\
influenced Auteur Profondeur_D'influence [vision] \n\
communaute Auteur Profondeur [vision] \n\
co-auteur Auteur [vision]\n\
chemin Auteur1 Auteur2" )

        rep=input("\nVoulez-vous continuer? (y/n)\n")
        if rep!=("y" or "Y"):
            continuer=False
        else:
            commande="Communaute.py "+input("Que voulez-vous lancer?\n./Communaute.py ")
            commande = commande.split(" ")
            print(commande)