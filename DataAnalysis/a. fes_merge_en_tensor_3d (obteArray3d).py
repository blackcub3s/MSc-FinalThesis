import os
import time
import numpy as np

def arregla_cagada():
	"""
	Si executes el makevector dos cops obtens fitxers total.txt que contenen més linies de les necessaries (make
	vector no esborra els fitxers anteriors sino que agafa els fitxers total.txt ja existents
	i els concatena... per tant, si vols tornar a executar-lo has de borrar els anteriors.

	M'ha sortit shape [93,642,140] i havia de sortir [93,214,140] >-->[SUB,ROIs,TS]. 
	Resulta que els fitxers total.txt que surten de makevector contenien el doble de ROIs (428) que les
	que haurien d'haver sortit (214) i el primer subjecte, resulta que treia (642) ROIs.

	Això s'ha produit perquè pre al primer arxiu vam executar el makevector 2 cops xD. I com que jo
	sense voler he executat el makevector 2 cops per a tots els arxius, per aquesta raó tenim el doble de linies
	de les que toquen als arxius total.txt (a excepció del primer, que n'hi ha el triple pel que hem dit).

	El make vector entenc que concatena les noves linies al mateix arxiu XDD total.txt en comptes de borrar 
	el total.txt que hi havia abans. 
	"""
	j = 0
	carpetes = os.listdir(os.getcwd())
	carpetes.sort()

	for carpeta in carpetes:
		if "." not in carpeta:
			j = j + 1
			os.chdir("./"+carpeta+os.sep+"tc")
			os.remove(os.getcwd()+os.sep+"total.txt")
			os.chdir("../../")
	print("Subjectes borrats:")
	return j

#print(arregla_cagada())



def fes_merge(n_timeseries):
	"""
	GUARDATS.
		arr_3d --> numpy ndarray amb shape [93,214,140] >-->[SUBJECTES, ROIsSHEN,TIME SERIES]
		ll_subs =  [SUBJECTE 1, SUBJECTE 2, ... , SUBJECTE 93]
		ll_uids = [UID 1, UID 2, ..., UID 93]


	NOTA:

		les llistes son LA INFO dels subjectes. son correlatives a la primera dimensio (dimensio de subjectes)
		de la matriu arr_3d.

		Qualsevol dels dos valors són útils per identificar els subjectes. UID es un identificador unic que hi ha
		per a cada escaner de l'ADNI. 


	"""
	j = 0
	carpetes = os.listdir(os.getcwd())
	carpetes.sort()
	ll_matriu_3d = []
	ll = []
	ll_subs = []
	ll_uids = []
	for carpeta in carpetes:
		if "." not in carpeta:
			j = j + 1
			ids = carpeta.split("__")

			#GUARDO ELS IDS DELS SUBJECTES I ELS LL_UIDS (correlatius a la primera dimensió de arr_3d)
			ll_subs += [ids[0]]
			ll_uids += [ids[1]]

			os.chdir("./"+carpeta+os.sep+"tc")
			print("Subjecte: "+carpeta)
			print("\n")
			ll_matriu_subjecte= []
			k = 0
			
			with open("total.txt","r") as f:
				for linia in f:
					k = k +1 
					ll_linia = linia.split() #fora salts de linia i espais
					
					for i in range(len(ll_linia)):
						ll_linia[i] = float(ll_linia[i]) #passem tipus de dades a real
					if not len(ll_linia) == n_timeseries:
						raise ValueError("Compte! Que el subjecte i escaner amb id "+carpeta+" \nno té les "+str(n_timeseries)+" time series que esperaves")
					ll_matriu_subjecte = ll_matriu_subjecte + [ll_linia] #ll_matriu_subjecte conte matriu (214,140) (ROIs, TS)

			print("Subj_escan "+carpeta+" || "+"TS (columnes): "+str(len(ll_matriu_subjecte[0]))," | ROIs (files): "+str(len(ll_matriu_subjecte)))
			os.chdir("../../")
			ll_matriu_3d = ll_matriu_3d + [ll_matriu_subjecte] #COMPROVA QUE TINGUI [93,214,140] >-->[SUB,ROIs,TS]
			ll = ll + [k] 
			#if j == 10:
			#	break
	print(len(ll_matriu_3d),len(ll_matriu_3d[0]),len(ll_matriu_3d[0][0])) 
	arr_3d = np.array(ll_matriu_3d) #COMPROVA QUE TINGUI [93,214,140] >-->[SUB,ROIs,TS]
	print("TOTS ELS SUBJECTES HAN DE TENIR ELS MATEIXOS VALORS EN CADA ELEMENT DE LA SEGUENT LLISTA. SI NO, CAL BORRAR TOTAL.TXT, REEXECUTAR MAKEVECTOR I TORNAR A EXECUTAR FES_MERGE")
	print(ll)

	#FINALMENT GUARDEM LA NUMPY ARRAY I TAMBÉ ELS NOMS DELS SUBJECTES I ELS UIDS DELS ESCANERS
	# EN LLISTES CONTINGUDES EN TXTS, CORRELATIVES A LA PRIMERA DIMENSIO DE ARR_3D (DIMENSIO STACK)
	np.save("__arr_ADNI_3d_preprocessada",arr_3d)
	f1 = open("__subjectes.txt","w")
	f2 = open("__uids.txt","w")

	for i in range(len(ll_subs)): #HAN DE TENIR LA MATEIXA LLARGARIA LES LLISTES LL_SUBS I LL_UIDS.
		f1.write(ll_subs[i]+'\n')
		f2.write(ll_uids[i]+'\n')
	f1.close()
	f2.close()
	return "\nshape array subjectes: "+str(arr_3d.shape)+"\nnresubjectes: "+str(len(ll_subs))+"\nnre uids: "+str(len(ll_uids))

print(fes_merge(140)) #Comprova que les times series son exactament les que posem al parametre de la funcio per a tots els subjectes. SI no fos el cas, es queixaria i donaria un VAlueerror


