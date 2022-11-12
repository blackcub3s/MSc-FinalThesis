# -*- coding: utf-8 -*-
"""
Created on Mon Mar 19 01:13:52 2018

@author: santi
"""

def posa_en_linia():
	"""
	Pillo el llistat de variables del fitxer spss provinent de adnimerge
	package i poso les variables en una mateixa fila per poder-les
	després introduir correctament al programa spss com a capçals o header
	de a base de dades.
	
	"""
	f = open("variables_adnimerge.txt","r")
	str_variables = f.readline().split('"')[0][:-1]+',' #la primera linia no te espai. la tracto ja
	for linia in f: #comença des de la segona linia
		linia = linia[:-1].split('"')[0].split(" ")[1]
		str_variables += linia+','
	
	print("nre variables pillades: {:.0f}".format(str_variables.count(",")),"\n")
	return str_variables
print(posa_en_linia())	 #el resultat del print, copia'l com a capçalera de mira_dades.py