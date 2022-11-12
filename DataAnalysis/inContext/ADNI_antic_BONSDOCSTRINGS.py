# -*- coding: utf-8 -*-
"""
Created on Thu Mar 29 19:36:53 2018

@author: santi

VAIG FER AQUEST PEGOTE FINS QUE NO VAIG SABER 
"""





def parseja_linia(linia_en_llista_fitxer):
	"""
	Parseja una linia. , treient les comes i les cometes simples.
	 Retorna una linia neta. L'utilitzo en diverses classes que obren csvs amb la mateixa estructura xunga
	 de cometes vestigials.
	"""
	llesca = linia_en_llista_fitxer[:-1].split('","')
	llesca = [llesca[0][1:]] + llesca[1:-1] + [llesca[-1][:-1]]  #trec el caracter " vestigial del primer element de la llista ("019_S_4293) i el del final (Original")
	return llesca


import pandas as pd


class Diagnostics:
	"""Dins l'apartat Download --> Study data --> Assesments diagnostics trobem tres fitxers. En aquesta
		classe implemento una funció (exceptuant init) per a cada fitxer.
	
		ADSXLIST.csv --> 	Diagnosis and Symptoms Checklist [ADNI1,GO,2] --> 
		BLCHANGE.csv --> 	Diagnostic Summary - Baseline Changes [ADNI1,GO,2,3] --> Aqui es captura conversio de l'enfermetat
		DXSUM_PDXCONV_ADNIALL.csv --> 	Diagnostic Summary [ADNI1,GO,2,3] --> Aqui hi ha baseline diagnosis
		Es recullen en un codi diferent en funció de l'etapa de l'estudi. A saber: 
			   - ADNI GO/2 --> baseline diagnosis -->recollit a la “DXCHANGE” variable. 
			   - ADNI1 --> baseline diagnosis --> can be obtained using the “DXCURREN” variable at VISCODE==”bl,” 
			 (TRET DE SECCIO FAQS) http://adni.loni.usc.edu/data-samples/data-faq/
		
		Aquesta classe no instancia res. A dins el mètode INIT obro els tres fitxers disponibles per a tenir-los
		
	"""
	def __init__(self):
		#OOMPTE, AQUESTOS FITXERS NO INCLOUEN INFO DE TOT PENSO!! OJO!! 
		self.diagnostics = open(".\Diagnosis_20.02.18\ADSXLIST.csv") # Diagnosis and Symptoms Checklist [ADNI1,GO,2]
		self.blchanges = open(".\Diagnosis_20.02.18\BLCHANGE.csv")   # Diagnostic Summary - Baseline Changes [ADNI1,GO,2,3]
		self.diag_summary = open(".\Diagnosis_20.02.18\DXSUM_PDXCONV_ADNIALL.csv") # Diagnostic Summary [ADNI1,GO,2,3]


	def obre_diagnostics(self):
		ll_diagnostics = self.diagnostics.readlines()
		capsal_diagnostics, ll_diagnostics = ll_diagnostics[0],ll_diagnostics[1:]
		
	
	
	def obre_canvis_liniabase(self):
		"""el DXCHANGE (POSICIO 9) te diagnostic linia base (adni go/2) 
			i el DXCURREN (POSICIO 10) te el diagnostic lina base (ADNI1)"""
		ll_canvis_lb = self.diagnostics.readlines()
		capsal_canvis_liniabase, ll_diagnostics = ll_canvis_lb[0], ll_canvis_lb[1:]

	
	def obre_resum_diagnostics(self):
		ll_resum_diagnostics = self.diag_summary.readlines()
		capsal_resum_diagnostics, ll_resum_diagnostics = ll_resum_diagnostics[0], ll_resum_diagnostics[1:]
		#PROVO ALGO AMB PANDAS
		df_dxsum = pd.read_csv(".\Diagnosis_20.02.18\DXSUM_PDXCONV_ADNIALL.csv")
		
		# EVALUO, DE  QUANTS MCIs es converteixen a ALZHEIMERS!! I quants de normal 
		#no varien, mira diapo 47 de slide_data_training_part_2.
		conta_conversions = 0
		conta_normals = 0
		conta_visites_bl = 0
		#MIRO VARIABE DXCHANGE, QUE CONTÉ CANVIS EN ELS DIAGNOSTICS. 
		for codi_diagnostic in df_dxsum["DXCHANGE"]:
			if codi_diagnostic == 5: #cas MCI --> AD
				conta_conversions = conta_conversions + 1
			elif codi_diagnostic == 1: #cas 1=Stable:NL to NL
				conta_normals = conta_normals + 1
		print("TIPUS VISITA __ CONTEIG\n", df_dxsum['VISCODE'].value_counts())
		print("conta visites base line: "+str(conta_visites_bl))
		print("total conversions MCI --> ALZ: {:.2f}".format(conta_conversions))
		print("total estbles en normalitat (NL --> NL): {:.2f}".format(conta_normals))
		
		#COM QUE ALGUNS DELS DIAGNOSTICS DE ADNI2 NO ESTAN POSATS A LA TAULA (cOM DIUEN A PAGINA 6 DE SLIDE_DATA
		#TRAINING, S'ACONSELLA TREURE EL DIAGNOSTIC FENT SERVIR LES VARIABLES 'VISCODE' -SI ES LINIA BASE, O NO O BLA BLA-
		# i 'RID', UN ID DE ALGO)
		
		#SEGUENT REPTE... VEURE QUANT TEMPS PASSA DES DE LA BASELINE FINS A LA CONVERSIÓ 
		#POSEM 'VISCODE' I 'RID' EN UNA MATEIXA LLISTA DE ESTRUCTURA ['VISCODE 1','RID_1],[VISCODE_2,'RID_2']
		ll_RID = list(df_dxsum['RID'])
		ll_VISCODE = list(df_dxsum['VISCODE'])
		
		ll_RID_VISCODE = []
		for i in range(len(ll_RID)):
			ll_RID_VISCODE += [[ll_RID[i], ll_VISCODE[i]]]
		print(ll_RID_VISCODE[-5:])			
			
		
		
		

#Diagnostics().obre_diagnostics()
#Diagnostics().obre_canvis_liniabase()
#Diagnostics().obre_resum_diagnostics()







class Neuropsychological:
	pass


























def troba_MCIs_a_AD(nomes_ADNI3):
	""" la gestio de les dades a l'ADNI és complicada. Quan ens baixem les dades
	    de "advanced search" tenim dos fitxers .csv per baixar (SENSE CONTAR ELS 
		FITXERS QUE CONTENEN LA PATOLOGIA DELS SUBJECTES
    	, QUE CALDRÀ INTERGRAR-LOS DESPRÉS, ni les de METADADADES). 
		Ambdós fitxers contenen informació complementària, però, com veurem, 
		en alguns casos redundant. 
		
		En fer la cerca avançada obtenim un fitxer com aquest (pestanya advanced
        search), que anomeno F1 [veure C en el full dades ADNI]:

			#CAPSALERA: "Subject ID","Sex","Age","Description","Type"
			#EXEMPLE: "941_S_6094","F","69.6","Axial rsfMRI (Eyes Open)","Original"
		
		No el farem servir.
		
		El que carreguem a    F2     és el que s'obté en guardar a 
    	la llista (pestanya data collections) [veure D en el full dades ADNI] i sí que 
		l'usarem:

			# CAPSALERA: "Image Data ID","Subject","Group","Sex","Age","Visit","Modality","Description","Type","Acq Date","Format","Downloaded"
			# EXEMPLE: "957990","116_S_6119","Patient","F","67","1","fMRI","MoCoSeries","Original","1/29/2018","DCM",""


		Noteu que a F2 s'hi conté tot lo important que hi ha a F1 (NOTA: no sé què és
		 "type"). El camp d'edat a F1 no té decimals,mentre que el camp d'edat de F2, sí.
		 Això és especialment important atès que no volem pas perdre una informació que pot suposar
		una diferència com a màxim de mig any (per exemple, per a fer analisis de subgrups o estratificar pot ser util
							    
		Per exemple un subjecte on això es veu és per al subjecte 4293,
		 avaluat al centre 019:

		Aquest subjecte té els seguents registres dins F1:

			019_S_4293	M	69.8	    Resting State fMRI	        Original
			019_S_4293	M	70		    Resting State fMRI	        Original
			019_S_4293	M	70.4	    Resting State fMRI	        Original
			019_S_4293	M	70.8        Resting State fMRI	        Original
			019_S_4293	M	71.9    	Resting State fMRI	        Original
			019_S_4293	M	73.8	    Extended Resting State fMRI	Original
			019_S_4293	M	75.4	    Axial 2D PASL	            Original
			019_S_4293	M	75.4	    Axial fcMRI (EYES OPEN)	    Original

		en canvi, a dins F2, el mateix subjecte té les edats arrodonides a l'enter més proper: 

			860222	019_S_4293		Patient	M	75	101	fMRI	Axial 2D PASL					Original	6/08/2017	DCM																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																					
			860227	019_S_4293		Patient	M	75	101	fMRI	Axial fcMRI (EYES OPEN)			Original	6/08/2017	DCM
			531790	019_S_4293		Patient	M	74	34	fMRI	Extended Resting State fMRI		Original	10/19/2015	DCM
			415196	019_S_4293		Patient	M	72	30	fMRI	Resting State fMRI				Original	11/13/2013	DCM
			343304	019_S_4293		Patient	M	71	28	fMRI	Resting State fMRI				Original	10/31/2012	DCM
			302671	019_S_4293		Patient	M	70	25	fMRI	Resting State fMRI				Original	5/09/2012	DCM
			277286	019_S_4293		Patient	M	70	24	fMRI	Resting State fMRI				Original	1/10/2012	DCM
			261984	019_S_4293		Patient	M	70	22	fMRI	Resting State fMRI				Original	10/20/2011	DCM

		
        Per solucionar això hi ha dues alternatives:
        
        L'alternativa complicada passa per unir ambdues taules és la que parteix del deseconeixement de l'existència
        de les metadades. Sí... a les metadades tenim l'edat amb força decimals (saltar la
		secció amb sangrat i seguir llegint sota la mateixa per veure l'alternativa senzilla)
            
                La idea, seria, doncs, afegir la informació "bona" de F1 (es a dir, l'edat amb un decimal) a
        		a F2 (on l'edat caldrà substituir-la, perquè només és entera).
        		Per a fer-ho cal afegir l'ID de cada subjecte en F1 com a clau d'un dic (d_f1) i per a cada clau, hi posarem
        		una llista que contindrà l'edat de les diverses sessions, i l'ordenarem.
        
        		AIxi doncs, per exemple, si fem:
        
        			print(d_f1['019_S_4293'])
        
        		tornarà:
        		
        			[69.8, 70.0, 70.4, 70.8, 71.9, 73.8, 75.4, 75.4]
        		
        		Un cpp fet d_f1, farem un segon dic (d_f2) que com a claus tindrà l'id del subjecte i com a
        		valor una llista amb subllistes, cada una de les quals representarà una sessio o fila
            	per a aquell subjecte determinat. Per exemple, d_f2 tindrà, entre, 
        		multiples claus aquesta "019_S_4293". Si busquem el valor que contindrà el diccionari
            	mitjançant:
        
        		d_f2['019_S_4293'] obtindrem, evidentment les dades anteriors pero amb 
				una estructura sense ids repetits [****]:
        
                    
                #IMAGE UID, SUBJECT IDENTIFIER, ?????, SEX, EDAT,VISITA,MODALITY, DESCRIPCIO, TIPUS, ACQ DATE, FORMAT, DOWNLOADED
        		{'019_S_4293' : 
        		   [['860222', '019_S_4293', 'Patient', 'M', '75', '101', 'fMRI', 'Axial 2D PASL', 'Original', '6/08/2017', 'DCM', ''], 
        			['860227', '019_S_4293', 'Patient', 'M', '75', '101', 'fMRI', 'Axial fcMRI (EYES OPEN)', 'Original', '6/08/2017', 'DCM', ''], 
        			['531790', '019_S_4293', 'Patient', 'M', '74', '34', 'fMRI', 'Extended Resting State fMRI', 'Original', '10/19/2015', 'DCM', ''], 
        			['415196', '019_S_4293', 'Patient', 'M', '72', '30', 'fMRI', 'Resting State fMRI', 'Original', '11/13/2013', 'DCM', ''], 
        			['343304', '019_S_4293', 'Patient', 'M', '71', '28', 'fMRI', 'Resting State fMRI', 'Original', '10/31/2012', 'DCM', ''], 
        			['302671', '019_S_4293', 'Patient', 'M', '70', '25', 'fMRI', 'Resting State fMRI', 'Original', '5/09/2012', 'DCM', ''], 
        			['277286', '019_S_4293', 'Patient', 'M', '70', '24', 'fMRI', 'Resting State fMRI', 'Original', '1/10/2012', 'DCM', ''], 
        			['261984', '019_S_4293', 'Patient', 'M', '70', '22', 'fMRI', 'Resting State fMRI', 'Original', '10/20/2011', 'DCM', '']]
        		}
            Un cop fet això, es tracta, donada la llista que hem posat abans ([69.8, 70.0, 70.4, 70.8, 71.9, 73.8, 75.4, 75.4])
            hi psoem els seus valors als punts corresponents del d_D2, substituint-los per les edats enteres. 
            
            No és res trivial, perquè no existeix una clau primària / forànea entre ambdues taules (molt 
            simpàtics els de l'ADNI). AIxí doncs, cal buscar una alternativa per substituir cada edat
            al lloc (persona i moment) que li pertoca: la solució passa per seguir l'ordre imposat per les dates
            d'adquisici dels escaners: EN qualsevol cas, dels escàners, podem utilitzar la funció vectoritza_dates
            de la classe creada Dates.
            
		D'altra banda, l'alternativa senzilla és la que simplement
        accedeix a les metadades (un altre conjunt de fitxers que et surt al moment de fer la la DESCÀRREGA de
        les dades i es baixa com un ZIP o RAR).
        
        De nou, dins l'arxiu que es baixa com a METADATA, et donen l'opció d'escollir dues modalitats per obtenir informació de cada subjecte en cada escàner... dades
        redundants. Per una banda tens:
            
            MODALITAT A:
            
                FITXERS .xml directes, amb la informació continguda en els strings de nom de fitxer. 
                
                exemple del nom del fitxer per al subjecte 019_S_42923 que veiem als exemples:
                    
                    "ADNI_019_S_4293_Axial_fcMRI__EYES_OPEN__S571713_I860227.xml"
                    
                On apareixen SUBJECT_UID   DESCRIPCIO        SERIESUID_IMAGEUID. 
                
                    NO sé què és SERIESUID, pero IMAGE UID ES EL QUE SURT A LA PRIMERA COLUMNA DE F2 (MODALITAT)
                    EN PRINCIPI imatge uid ÉS PERFECTE COM A CLAU PRIMARIA de la taula, i servirà per 
                    associar les claus DEL d_F2 obtingudes del fitxer F2 .
        
                Dins de cada fitxer HTML tens moltíssima informació, molta de la qual no trobes en altres bandes. 
                D'aquí, de dins el fitxer .xml de la modalitat A, extreurem l'edat exacta de la persona.
                TAmbé enumerem altres camps que podrien ser-nos importants i que NO son redundants. Entre 
                claudators hi ha els que usarem si o si.
                
                                 [[ <imageUID>860227</imageUID>  ]]
                                 [[ <subjectAge>75.3833</subjectAge>  ]]
                                    <visitIdentifier>ADNI3 Initial Visit-Cont Pt</visitIdentifier>
                                    <weightKg>95.0</weightKg>
                                    <protocolTerm>
                                        <protocol term="Field Strength">3.0</protocol>
                                        trens slices, slice thickness, puslse sequence... etc...
                                        
                                        
                                        
                    nota (la primera columna de F2 i el conjunt de tots els nombres emplaçats dins
                    les etiquetes dels IMAGE UID ()  formen relació de 1 a 1 (per tant podem treure la informacio
                    considerant-les que son una relació clau primarea / foranea i unir-les)
                    

                    
                    D'aqui també pots extreure 
                    
                    els fitxers
                    .xml de la modalitat A )
                    <imageUID>860227</imageUID>
                        
    
                    <subjectAge>75.3833</subjectAge>
                    
                    
        
        Tens la modalitat     A     
        Una de les dues conté més informació que l'altra. La que conté més
        informació és la que té les metadades (fitxers .xml, amb les típiques etiquetes HTML) 
        
        
	"""
	#miro fitxers que contenen nomes dades de fMRI de l'ADNI3 (les que estic descarregant ara)
	if nomes_ADNI3: 
		f2 = open ("fMRI_ADNI3_2_13_2018.csv","r")
		
	#contenen tota fMRI de l'ADNI de les dates mencionades 
	else:			
		f2 = open("ADNI_tots_fMRI_tots_2_13_2018.csv","r") #obtingut de "data collections". de la coleccio "Totes_les_FMRI_s"]

	#Trec capçaleres i passo a llista
	next(f2)
	ll_linies_f2 = f2.readlines()

	##### PAS 2 ) # PASSEM LA LLISTA DE LA LLISTA QUE CONTÉ F2, A DICCIONARI (d_f2) 
    				# AMB UNA ESTRUCTURA DE CLAU PRIMARIA NO REPETIDA (SUBJECT ID) 
                 # VEURE [****]
	d_f2 = {}
	for i in range(len(ll_linies_f2)):
		subjecte_ID_f2 = ll_linies_f2[i][1]
		if not subjecte_ID_f2 in d_f2:
			d_f2[subjecte_ID_f2] = [ll_linies_f2[i]]
		else:
			d_f2[subjecte_ID_f2] = d_f2[subjecte_ID_f2] + [ll_linies_f2[i]]
	
	print(d_f2['019_S_4293'],len(d_f2['019_S_4293']))
 	
    
    
    #### PAS 3) # SUBSTITUIM LES EDATS ARRODONIDES PROVINENTS DE F2 PER LES EDATS GUAYS
    # , AMB DECIMALS, OBTINGUDES DE F1. 
    ####
    
    ####
    # NOTA: PER A FER-HO FEM SERVIR LES DATES D'ADQUISICIÓ DELS ESCANERS QUE, EVIDENTMENT,
    # GENEREN UNA ORDENACIÓ QUE NO ES POT OBTENIR DE CAP ALTRA MANERA. ELS DIES ES REGISTREN
    # EN FORMAT MM/DD/AAAA, PERO DELS MESOS 1 A 9, ES FA EN M/DD/AAAA
    ####

	return d_f2




















		


def ajunta_els_dos_CSV(nomes_ADNI3):
	""" la gestio de les dades a l'ADNI és complicada. Quan ens baixem les dades
	    de "advanced search" tenim dos fitxers .csv per baixar (SENSE CONTAR ELS 
		FITXERS QUE CONTENEN LA PATOLOGIA DELS SUBJECTES
    	, QUE CALDRÀ INTERGRAR-LOS DESPRÉS, ni les de METADADADES). 
		Ambdós fitxers contenen informació complementària, però, com veurem, 
		en alguns casos redundant. 
		
		El fitxer que carreguem a    F1     és el que s'obté en fer
    	la cerca avançada (pestanya advanced search) [veure C en el full dades ADNI]:

			#CAPSALERA: "Subject ID","Sex","Age","Description","Type"
			#EXEMPLE: "941_S_6094","F","69.6","Axial rsfMRI (Eyes Open)","Original"
		
		El que carreguem a    F2     és el que s'obté en guardar a 
    	la llista (pestanya data collections) [veure D en el full dades ADNI]

			# CAPSALERA: "Image Data ID","Subject","Group","Sex","Age","Visit","Modality","Description","Type","Acq Date","Format","Downloaded"
			# EXEMPLE: "957990","116_S_6119","Patient","F","67","1","fMRI","MoCoSeries","Original","1/29/2018","DCM",""


		Noteu que a F2 s'hi conté tot lo important que hi ha a F1 (NOTA: no sé què és "type"). EL que passa és que el camp d'edat a F1 no té decimals,
		mentre que el camp d'edat de F2, sí. Això és especialment important atès que no volem pas perdre una informació que pot suposar
		una diferència com a màxim de mig any (per exemple, per a elaborar hipòtesis pronòstiques).

		Per exemple un subjecte on això es veu és per al subjecte 4293, avaluat al centre 019:

		Aquest subjecte té els seguents registres dins F1:

			019_S_4293	M	69.8	    Resting State fMRI	        Original
			019_S_4293	M	70		    Resting State fMRI	        Original
			019_S_4293	M	70.4	    Resting State fMRI	        Original
			019_S_4293	M	70.8        Resting State fMRI	        Original
			019_S_4293	M	71.9    	Resting State fMRI	        Original
			019_S_4293	M	73.8	    Extended Resting State fMRI	Original
			019_S_4293	M	75.4	    Axial 2D PASL	            Original
			019_S_4293	M	75.4	    Axial fcMRI (EYES OPEN)	    Original

		en canvi, a dins F2, el mateix subjecte té les edats arrodonides a l'enter més proper: 

			860222	019_S_4293		Patient	M	75	101	fMRI	Axial 2D PASL					Original	6/08/2017	DCM																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																					
			860227	019_S_4293		Patient	M	75	101	fMRI	Axial fcMRI (EYES OPEN)			Original	6/08/2017	DCM
			531790	019_S_4293		Patient	M	74	34	fMRI	Extended Resting State fMRI		Original	10/19/2015	DCM
			415196	019_S_4293		Patient	M	72	30	fMRI	Resting State fMRI				Original	11/13/2013	DCM
			343304	019_S_4293		Patient	M	71	28	fMRI	Resting State fMRI				Original	10/31/2012	DCM
			302671	019_S_4293		Patient	M	70	25	fMRI	Resting State fMRI				Original	5/09/2012	DCM
			277286	019_S_4293		Patient	M	70	24	fMRI	Resting State fMRI				Original	1/10/2012	DCM
			261984	019_S_4293		Patient	M	70	22	fMRI	Resting State fMRI				Original	10/20/2011	DCM

		
        Per solucionar això hi ha dues alternatives:
        
        L'alternativa complicada per unir ambdues taules és la que parteix del deseconeixement de l'existència
        de les metadades. Sí... la vaig pensar perquè no sabia que hi havia les metadades. 
        T'estalvio, doncs, el suplici d'haver de llegir la solució.
            
                La idea, seria, doncs, afegir la informació "bona" de F1 (es a dir, l'edat amb un decimal) a
        		a F2 (on l'edat caldrà substituir-la, perquè només és entera).
        		Per a fer-ho cal afegir l'ID de cada subjecte en F1 com a clau d'un dic (d_f1) i per a cada clau, hi posarem
        		una llista que contindrà l'edat de les diverses sessions, i l'ordenarem.
        
        		AIxi doncs, per exemple, si fem:
        
        			print(d_f1['019_S_4293'])
        
        		tornarà:
        		
        			[69.8, 70.0, 70.4, 70.8, 71.9, 73.8, 75.4, 75.4]
        		
        		Un cpp fet d_f1, farem un segon dic (d_f2) que com a claus tindrà l'id del subjecte i com a
        		valor una llista amb subllistes, cada una de les quals representarà una sessio o fila
            	per a aquell subjecte determinat. Per exemple, d_f2 tindrà, entre, 
        		multiples claus aquesta "019_S_4293". Si busquem el valor que contindrà el diccionari
            	mitjançant:
        
        		d_f2['019_S_4293'] obtindrem, evidentment les dades anteriors pero amb 
				una estructura sense ids repetits [****]:
        
                    
                #IMAGE UID, SUBJECT IDENTIFIER, ?????, SEX, EDAT,VISITA,MODALITY, DESCRIPCIO, TIPUS, ACQ DATE, FORMAT, DOWNLOADED
        		{'019_S_4293' : 
        		   [['860222', '019_S_4293', 'Patient', 'M', '75', '101', 'fMRI', 'Axial 2D PASL', 'Original', '6/08/2017', 'DCM', ''], 
        			['860227', '019_S_4293', 'Patient', 'M', '75', '101', 'fMRI', 'Axial fcMRI (EYES OPEN)', 'Original', '6/08/2017', 'DCM', ''], 
        			['531790', '019_S_4293', 'Patient', 'M', '74', '34', 'fMRI', 'Extended Resting State fMRI', 'Original', '10/19/2015', 'DCM', ''], 
        			['415196', '019_S_4293', 'Patient', 'M', '72', '30', 'fMRI', 'Resting State fMRI', 'Original', '11/13/2013', 'DCM', ''], 
        			['343304', '019_S_4293', 'Patient', 'M', '71', '28', 'fMRI', 'Resting State fMRI', 'Original', '10/31/2012', 'DCM', ''], 
        			['302671', '019_S_4293', 'Patient', 'M', '70', '25', 'fMRI', 'Resting State fMRI', 'Original', '5/09/2012', 'DCM', ''], 
        			['277286', '019_S_4293', 'Patient', 'M', '70', '24', 'fMRI', 'Resting State fMRI', 'Original', '1/10/2012', 'DCM', ''], 
        			['261984', '019_S_4293', 'Patient', 'M', '70', '22', 'fMRI', 'Resting State fMRI', 'Original', '10/20/2011', 'DCM', '']]
        		}
            Un cop fet això, es tracta, donada la llista que hem posat abans ([69.8, 70.0, 70.4, 70.8, 71.9, 73.8, 75.4, 75.4])
            hi psoem els seus valors als punts corresponents del d_D2, substituint-los per les edats enteres. 
            
            No és res trivial, perquè no existeix una clau primària / forànea entre ambdues taules (molt 
            simpàtics els de l'ADNI). AIxí doncs, cal buscar una alternativa per substituir cada edat
            al lloc (persona i moment) que li pertoca: la solució passa per seguir l'ordre imposat per les dates
            d'adquisici dels escaners: EN qualsevol cas, dels escàners, podem utilitzar la funció vectoritza_dates
            de la classe creada Dates.
            
		D'altra banda, l'alternativa senzilla és la que simplement
        accedeix a les metadades (un altre conjunt de fitxers que et surt al moment de fer la la DESCÀRREGA de
        les dades i es baixa com un ZIP o RAR).
        
        De nou, dins l'arxiu que es baixa com a METADATA, et donen l'opció d'escollir dues modalitats per obtenir informació de cada subjecte en cada escàner... dades
        redundants. Per una banda tens:
            
            MODALITAT A:
            
                FITXERS .xml directes, amb la informació continguda en els strings de nom de fitxer. 
                
                exemple del nom del fitxer per al subjecte 019_S_42923 que veiem als exemples:
                    
                    "ADNI_019_S_4293_Axial_fcMRI__EYES_OPEN__S571713_I860227.xml"
                    
                On apareixen SUBJECT_UID   DESCRIPCIO        SERIESUID_IMAGEUID. 
                
                    NO sé què és SERIESUID, pero IMAGE UID ES EL QUE SURT A LA PRIMERA COLUMNA DE F2 (MODALITAT)
                    EN PRINCIPI imatge uid ÉS PERFECTE COM A CLAU PRIMARIA de la taula, i servirà per 
                    associar les claus DEL d_F2 obtingudes del fitxer F2 .
        
                Dins de cada fitxer HTML tens moltíssima informació, molta de la qual no trobes en altres bandes. 
                D'aquí, de dins el fitxer .xml de la modalitat A, extreurem l'edat exacta de la persona.
                TAmbé enumerem altres camps que podrien ser-nos importants i que NO son redundants. Entre 
                claudators hi ha els que usarem si o si.
                
                                 [[ <imageUID>860227</imageUID>  ]]
                                 [[ <subjectAge>75.3833</subjectAge>  ]]
                                    <visitIdentifier>ADNI3 Initial Visit-Cont Pt</visitIdentifier>
                                    <weightKg>95.0</weightKg>
                                    <protocolTerm>
                                        <protocol term="Field Strength">3.0</protocol>
                                        trens slices, slice thickness, puslse sequence... etc...
                                        
                                        
                                        
                    nota (la primera columna de F2 i el conjunt de tots els nombres emplaçats dins
                    les etiquetes dels IMAGE UID ()  formen relació de 1 a 1 (per tant podem treure la informacio
                    considerant-les que son una relació clau primarea / foranea i unir-les)
                    

                    
                    D'aqui també pots extreure 
                    
                    els fitxers
                    .xml de la modalitat A )
                    <imageUID>860227</imageUID>
                        
    
                    <subjectAge>75.3833</subjectAge>
                    
                    
        
        Tens la modalitat     A     
        Una de les dues conté més informació que l'altra. La que conté més
        informació és la que té les metadades (fitxers .xml, amb les típiques etiquetes HTML) 
        
        
	"""
	#miro fitxers que contenen nomes dades de fMRI de l'ADNI3 (les que estic descarregant ara)
	if nomes_ADNI3: 
		f1 = open("idaSearch_2_13_2018_fMRI_nomes_ADNI3.csv","r") 
		f2 = open ("fMRI_ADNI3_2_13_2018.csv","r")
	
	#contenen tota fMRI de l'ADNI de les dates mencionades 
	else:			
		f1 = open("idaSearch_2_13_2018.csv","r")  #[Obtingut al moment de fer la cerca]
		f2 = open("ADNI_tots_fMRI_tots_2_13_2018.csv","r") #obtingut de "data collections". de la coleccio "Totes_les_FMRI_s"]

	#Trec capçaleres
	next(f1)
	next(f2)
	
	
	#assigno cada registre a cada llista
	ll_linies_f1 = f1.readlines()
	ll_linies_f2 = f2.readlines()
	
	if len(ll_linies_f1) == len(ll_linies_f2):
		print("els dos fitxers tenen la mateixa long. correcte")
	else:
		raise ValueError("ep! Que els dos fitxers no tenen la mateixa longitud! En algun dels dos tens un escaner de més!")

	


	# CREO el diccionari d_f1.
	# (conte ID subjecte COM A CLAU + l'edat (o bé edats en cas que hi hagi múltiples escaners) amb decimal en el moemnt en que li fan 
	# escaners.
	d_f1 = {}

	
	

	###### PAS 1 )    PARSEJEM FITXER F1 I EXTRAIEM LA INFORMACIO EN UN DICCIONARI AMB ELS IDS DELS SUUBJECTRES COM A CLAUS
	for i in range(len(ll_linies_f1)):
		# trec salts de linia i separo els strings per ",", posant-los en una llista com es fa sempre.
		
		ll_linies_f1[i] = parseja_linia(ll_linies_f1[i])
		ll_linies_f2[i] = parseja_linia(ll_linies_f2[i])

		#print(ll_linies_f2[i])

		
		#PILLO IDS I EDATS [UNIQUES INFORMACIONS NO REDUNDANTS]
		subjecte_ID_f1 = ll_linies_f1[i][0]
		edat_f1 = float(ll_linies_f1[i][2])

		if not subjecte_ID_f1 in d_f1:
			d_f1[subjecte_ID_f1] = [edat_f1]
		else:
			d_f1[subjecte_ID_f1] = d_f1[subjecte_ID_f1] + [edat_f1]

	#ordeno les llistes que hi ha com a valors.ja estan ordenats pel que veig,
	# però per si les mosques...
	for c in d_f1:
		d_f1[c].sort()
	
    
    
    

	##### PAS 2 ) # PASSEM LA LLISTA DE LA LLISTA QUE CONTÉ F2, A DICCIONARI (d_f2) 
    				# AMB UNA ESTRUCTURA DE CLAU PRIMARIA NO REPETIDA (SUBJECT ID) 
                 # VEURE [****]
	d_f2 = {}
	for i in range(len(ll_linies_f2)):
		subjecte_ID_f2 = ll_linies_f2[i][1]
		if not subjecte_ID_f2 in d_f2:
			d_f2[subjecte_ID_f2] = [ll_linies_f2[i]]
		else:
			d_f2[subjecte_ID_f2] = d_f2[subjecte_ID_f2] + [ll_linies_f2[i]]
	
	print(d_f2['019_S_4293'],len(d_f2['019_S_4293']))
 	
    
    
    #### PAS 3) # SUBSTITUIM LES EDATS ARRODONIDES PROVINENTS DE F2 PER LES EDATS GUAYS
    # , AMB DECIMALS, OBTINGUDES DE F1. 
    ####
    
    ####
    # NOTA: PER A FER-HO FEM SERVIR LES DATES D'ADQUISICIÓ DELS ESCANERS QUE, EVIDENTMENT,
    # GENEREN UNA ORDENACIÓ QUE NO ES POT OBTENIR DE CAP ALTRA MANERA. ELS DIES ES REGISTREN
    # EN FORMAT MM/DD/AAAA, PERO DELS MESOS 1 A 9, ES FA EN M/DD/AAAA
    ####

	return d_f2



	print("\nF2")
	print(ll_linies_f2[0])
	print(ll_linies_f2[1])

	print("\nF1")
	print(ll_linies_f1[0])
	print(ll_linies_f1[1])


#print(ajunta_els_dos_CSV(nomes_ADNI3 = False))



