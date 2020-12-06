# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 19:20:44 2020

@author: Thomas
"""


import csv
import re


cheminLecture=""
cheminEcriture=""


def getChemin(choix):
    with open('config.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='\n')
        next(spamreader) #ignore la première ligne
        for ligne in spamreader:
            esp = re.split(",",ligne[0])
            if choix == "lecture":
                return esp[0]
            if choix == "ecriture":
                return esp[1]
            return 0





























































