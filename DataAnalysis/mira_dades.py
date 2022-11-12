import datetime
import time
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd




class Csv_apartat_data_collections:
	"""
	INPUT: Fitxer .csv de data collections. Estructura de fitxer
	# CAPSALERA: "Image Data ID","Subject","Group","Sex","Age","Visit","Modality","Description","Type","Acq Date","Format","Downloaded"
	# EXEMPLE: "957990","116_S_6119","Patient","F","67","1","fMRI","MoCoSeries","Original","1/29/2018","DCM",""

	"""
	def __init__(self,nom_fitxer):
		self.nom_fitxer = nom_fitxer
		self.f2 = open(nom_fitxer,"r")
	
	def parseja_i_posa_a_diccionari(self,CONTA_SUBJECTES, MODALITATS_NEUROIMATGE):
		"""
		cada linia del fitxer CSV que parsejem es un escàner per a un subjecte donat. 
		M'interessa tenir cada subjecte (com a clau) en un diccionari
		TROS INPUT (SUBJECTE 019_S_4293). FALTA POSAR LES COMETES... Xd
		   
		   #IMAGE UID, SUBJECT IDENTIFIER, ?????, SEX, EDAT,VISITA,MODALITY, DESCRIPCIO, TIPUS, ACQ DATE, FORMAT, DOWNLOADED
			"860222","019_S_4293","Patient","M","75","101","fMRI","Axial 2D PASL"					Original	6/08/2017	DCM																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																					
			"860227","019_S_4293","Patient","M","75","101","fMRI","Axial fcMRI (EYES OPEN)"			Original	6/08/2017	DCM
			"531790","019_S_4293","Patient","M","74","34","fMRI","Extended Resting State fMRI"		Original	10/19/2015	DCM


		TROS OUTPUT:
					 #IMAGE UID, SUBJECT IDENTIFIER, ?????, SEX, EDAT,VISITA,MODALITY, DESCRIPCIO, TIPUS, ACQ DATE, FORMAT, DOWNLOADED
			{'019_S_4293' : 
        		   [['860222', '019_S_4293', 'Patient', 'M', '75', '101', 'fMRI', 'Axial 2D PASL', 'Original', '6/08/2017', 'DCM', ''], 
        			['860227', '019_S_4293', 'Patient', 'M', '75', '101', 'fMRI', 'Axial fcMRI (EYES OPEN)', 'Original', '6/08/2017', 'DCM', ''], 
        			['531790', '019_S_4293', 'Patient', 'M', '74', '34', 'fMRI', 'Extended Resting State fMRI', 'Original', '10/19/2015', 'DCM', '']]
        		}

			ARTGUMENTS: CONTA SUBJECTES: Si es TRUE te'ls conta i te'ls diu.
			
			"""
		#LA CAPSALERA POTS USARLA DESPRES PER FER UN PANDAS DATAFRAME
		ll_linies_f2 = self.f2.readlines()
		global capsalera_f2 #la faig global perque probablement la usare fora la classe
		capsalera_f2, ll_linies_f2 = ll_linies_f2[0], ll_linies_f2[1:]


		#PASSEM LA LLISTA QUE CONTE EL QUE ABANS ERA UN CSV A DICCIONARI (d_f2) 
		#AMB UNA ESTRUCTURA DE CLAU PRIMARIA NO REPETIDA (SUBJECT ID)
		d_f2 = {}
		for i in range(len(ll_linies_f2)):
			ll_linies_f2[i] = parseja_linia(ll_linies_f2[i])
			subjecte_ID_f2 = ll_linies_f2[i][1]
			if not subjecte_ID_f2 in d_f2:
				d_f2[subjecte_ID_f2] = [ll_linies_f2[i]]
			else:
				d_f2[subjecte_ID_f2] = d_f2[subjecte_ID_f2] + [ll_linies_f2[i]]
		
		if CONTA_SUBJECTES:	
			#UTILITZAT PER A FER DIAGRAMA DE FLUX
			print("al fitxer "+self.nom_fitxer+" hi ha un total de "+str(len(d_f2))+" persones.")
		d_conta = {}
		if MODALITATS_NEUROIMATGE:
			#CONTO QUINES I QUANTES N'HI HA EN TOTAL (NO MIRA SUBMODALITATS NEUROIMATGE!)
			for clau in d_f2:
				for linia_info_neuroimatge in d_f2[clau]:
					if not linia_info_neuroimatge[6] in d_conta:
						d_conta[linia_info_neuroimatge[6]] = 1
					else:
						d_conta[linia_info_neuroimatge[6]] = d_conta[linia_info_neuroimatge[6]] + 1
			print("\nmodalitats neuroimatge i nombre d'escaners de cada tipus:")
			print(d_conta)
		#print("NRE TOTAL SUBBJECTES A d_F2: "+ str(len(d_f2)))
		return d_f2




class Dates:
	"""pilla una llista de 
	strings amb dates de format mm/dd/aaaa o be m/dd/aaaa 
	i defineix metodes per a elles. O sigui, instancia la classe amb una llista de strings tipo
	["10/16/2011","10/14/2011","10/22/2011","10/13/2011"]"""
	def __init__(self,ll_dates):
		self.ll_dates = ll_dates
        
	def talla_i_reordena_dates(self):
		for i in range(len(self.ll_dates)):
			self.ll_dates[i] = self.ll_dates[i].split("/")
			for j in range(len(self.ll_dates[i])):
				self.ll_dates[i][j] = int(self.ll_dates[i][j])
		ll_dates_reordenades = []
		for subllista_data in self.ll_dates:
			mes,dia,anny = subllista_data
			ll_dates_reordenades = ll_dates_reordenades + [[anny,mes,dia]] 
		return ll_dates_reordenades #surt amb enters, en format [[2017,01,26],[2016,03,18],...]
    
	def vectoritza_dates(self):
		"""
		donada ll_dates_reordenades feta a la funcio "talla_data", en retorna
		una altra que conté les diferències en dies amb respecte a la data més petita de la llista.
		Així doncs, la data més petita té un 0 (l'origen) i les seguents tenen la diferencia
		 amb respecte a la inicial.
		 
		"""
		
		ll_dates_vectors = []
		ll_dates_reordenades = Dates.talla_i_reordena_dates(self)
		for data_empaquetada in ll_dates_reordenades:
			anny,mes,dia = data_empaquetada
			data_time_delta = datetime.datetime(anny,mes,dia)
			ll_dates_vectors = ll_dates_vectors + [data_time_delta]
		#ara ll_dates_vectors conte timedeltas. en faig una copia!
		array_dates_vectors = np.array(ll_dates_vectors[:])
		DATA_ORIGEN_timedelta = array_dates_vectors[np.argmin(array_dates_vectors)]   #DATA DE REFERENCIA. ORIGEN VECTOR FICTICI DE TEMPS PER SUBJECTE. ES EN RELACIO A LA QUAL FEM TOTES LES DIFERENCIES!
		
		#ara calculo les diferencies de cada data i faig nova llista:
		ll_diferencies = []
		for i in range(len(ll_dates_vectors)):
			ll_diferencies = ll_diferencies + [int((ll_dates_vectors[i] - DATA_ORIGEN_timedelta).total_seconds()/86400)]
		return ll_diferencies
    		
		
		#faig diferencies per cada time delta en relacio al timedelta definit
		#com a DATA_ORIGEN
		

#print(Dates(["10/16/2011","10/14/2011","10/22/2011","10/13/2011"]).vectoritza_dates())
# tornara, en aquest cas, les diferencies
# en dies, de forma relativa a les dates
# mateix ordre que l'entrada [3,1,9,0] 

#time.sleep(1)



 
def parseja_linia(linia_en_llista_fitxer):
	"""
	Parseja una linia. treient les comes i les cometes simples.
	Retorna una linia neta. L'utilitzo en diverses classes que obren csvs amb la mateixa estructura xunga de cometes vestigials.
	"""
	llesca = linia_en_llista_fitxer[:-1].split('","')
	llesca = [llesca[0][1:]] + llesca[1:-1] + [llesca[-1][:-1]]  #trec el caracter " vestigial del primer element de la llista ("019_S_4293) i el del final (Original")
	return llesca 
 
 
def subjectes_a_borrar():
	f = open("borrables_de_2.13.18.txt", "r")	
	sub = f.readlines()
	ll=[]
	for per in sub:
	    ll = ll + [per[:-1]]
	f.close()
	return ll

def posa_a_dict(index_clau_primaria, ll):
	d = {}
	for i in range(len(ll)):
		subjecte_ID = ll[i][index_clau_primaria]
		if not subjecte_ID in d:
			d[subjecte_ID] = [ll[i]]
		else:
			d[subjecte_ID] = d[subjecte_ID] + [ll[i]]
	return d

def posa_a_dict_2(escaner,d):
	if not escaner in d:
		d[escaner] = 1
	else:
		d[escaner] = d[escaner] + 1
	return d

def IMPORTANT_depura_ADNI_MERGE_i_ARXIU_fMRIs():
	"""
	Aquesta funció agafa dos CSV. Per una banda un amb les dades de la data d'adquisicio
	de les fMRIs i la tipologia de l'fMRI (ADNI_tots_fMRI_tots_2_13_2018.csv) 
	i per l'altra un altre amb els diagnòstics (adnimerge_NOMS_VARIABLES_POSATS.csv) 
	on hi ha informació sobre els diagnòstics de la 
	baseline i sobre quan els diagnostics canvien o no canvien amb el temps.
	
	La funció depura les dades per als dos fitxers. Això és: 
		
	1) Elimina subjectes de adnimerge_NOMS_VARIABLES_POSATS.csv que no poden estar
	de cap manera a ADNI_tots_fMRI_tots_2_13_2018, perquè el primer fitxer fou descarregat
	posteriorment a la data de descàrrega de la creació de la llista d'FMRI descarregada i, per tant
	el fitxer ADNI_tots_fMRI_tots_2_13_2018. En resum, elimina subjectes que no son cagades
	de l'adni. SIno que no hi han de ser perque no en tenim la fmri perque no l'haurem descarregat.					
		
	2) elimina subjectes que no estan als dos datasets i elimina aquells (s'elimnen als dos) que no tenen un diagnòstic a 
	la baseline (que és essencial per fer el model pronòstic, ja que el diagnostica a la baseline
	és el diagnòstic més segur, el que va a missa).
	
	3) També fa un gràfic de com va disminuint la població de l'ADNI al llarg del temps.
	I va fent prints en pantalla per veure el que vaig fent (no ho intentis entendre en dos dies xD)
	
	RETURNS: 
		
	dos diccionaris amb les dades amb aplicació bijectiva, perfectament depurades. Amb les mateixes
	claus (IDS_subjecte: (rollo 008_S_993)) i valors (llistes que tenen, com a subllistes, totes les sessions
	corresponent a cada subjecte). 
		
	    dic_valors_amerge --> (PROVÉ DE adnimerge_NOMS_VARIABLES_POSATS.csv
	    dic_subjectes_fMRIs-> ADNI_tots_fMRI_tots_2_13_2018.csv
	
	dos pandas dataframes amb les mateixes dades que ELS DOS DICCIONARIS ANTERIORS
	pero amb una fila per cada sessio d'imatge o diagnòstic. Estan guardats de maneres diferents
	doncs
	
		 df_amerge
		 df_fMRI
	################################################################### 
	#					          DICCIONARI             PANDAS DATAFRAME  #
	#   INFO ADNIMERGE    dic_valors_amerge            df_amerge      #
	#   INFO fMRIs        dic_subjectes_fMRIs          df_fMRI        #
	###################################################################  
	
	INFO ADNI MERGE --> te informacio diagnostics, mesos diagnostics, APOE, questionaris...
	INFO fMRIs --> Conté informació sobre les dates d'adquisicio de les fMRI, sobre
					el tipus d'FMRI usat
	
	
	"""
	
	# CARREGO DATAFRAME AMB TOTES LES DADES (ENTRE ALTRES DIAGNOSTIQUES!). 
	nomfitxer = "adnimerge_NOMS_VARIABLES_POSATS.csv"
	df_amerge = pd.read_csv("./Diagnosis_20.02.18/FES MERGE_AMB_DXSUM/ADNIMERGE_SPSS/adnimerge/"+nomfitxer) #dtype object fa que no surti l'advertència de la memòria

	#CARREGO EL DICCIONARI DE SUBJECTES DEL FITXER DE INFO DE LES FMRIS DEL FEBRER
	dic_subjectes_fMRIs = Csv_apartat_data_collections("ADNI_tots_fMRI_tots_2_13_2018.csv").parseja_i_posa_a_diccionari(CONTA_SUBJECTES=False, MODALITATS_NEUROIMATGE = False)
	
	
	#PASSO DATAFRAME AMERGE A LLISTA DE LLISTES DE VALORS PER FER EL DICT I TREC ELS NOMS DE LES VARIABLES PER NO PERDRELS
	ll_valors_amerge, ll_capsalera_amerge = df_amerge.values.tolist(), df_amerge.columns.tolist()
	#PASSO A DICCIONARI (AMB CLAUS COM A NOMBRE DE SUBJECTE I COM A VALORS LES SUBLLISTES DE CADA VISITA DEL SUBJECTE)
	dic_valors_amerge = posa_a_dict(3, ll_valors_amerge)
	
	
	#GUARDO CAPSALERA_fMRIs
	with open("ADNI_tots_fMRI_tots_2_13_2018.csv","r") as fitxer:
		ll_capsalera_fMRIs = parseja_linia(fitxer.readline())

	#POSEM DE NOU EL FITXER DIAGNOSTIC EN UN DATAFRAME, PERO ARA JA DEPURADET! 
	# TOTS ELS QUE SURTEN ARA A DF_AMERGE TENEN ALGUNA RESSONANCIA FUNCIONAL!!
	print("FLOW_DIAGRAM__nombre de pacients sotmesos a com a minim una fMRI: {:.0f}".format(len(dic_subjectes_fMRIs)))
	
	
	
	# OBJECTIU SEGUENT: DEIXAR dic_valors_amerge I dic_subjectes_fMRIs amb APLICACIO
	# BIJECTIVA ENTRE les seves claus (subjectes). I REPORTAR ELS MISSINGS (PASSOS 1 A 4).
	
	
	# PAS 1: AMERGE ÉS UN FITXER MÉS RECENT QUE EL FITXER DEL QUAL PROVE
	# DIC_SUBJECTE_FMRIS. ESBORREM TOTS ELS QUE ESTAN A ll_valors_amerge A PARTIR DE 13/02/2018.
	for subjecte_futur in subjectes_a_borrar():
		del dic_valors_amerge[subjecte_futur]
	
	print("DIAGRAMA DE FLUX:  total subjectes al fitxer d'info diagnostica: {:.0f}".format(len(dic_valors_amerge)))


	
	#CONTO, DELS SUBJECTES QUE HI HA A ADNIMERGE AMB ALGUN DIAGNOSTIC, QUANTS TENEN EL DIAGNOSTIC DE LA BASELINE
	conta_bl = 0
	conta_bl_dxBL = 0
	elimina_missings_diagnostics_ADNIMERGE = [] #guardo subjectes problematics que tenen missings al diagnostic DX.BX de la baseline. NO SERVEIXEN PER A RES!
	DX_BL_POSSIBLES = [1,2,3,4,5,6]
	for clau_subjecte in dic_valors_amerge:
		for sessio in dic_valors_amerge[clau_subjecte]:
			if sessio[5] == "bl":
				conta_bl = conta_bl + 1
				if sessio[7] in DX_BL_POSSIBLES:
					conta_bl_dxBL += 1 
				else:
					elimina_missings_diagnostics_ADNIMERGE += [clau_subjecte]
			break
	
	print(elimina_missings_diagnostics_ADNIMERGE)
	
	print("pacients que tinguin bl com a viscode (tenen una baseline visit) {:.0f}".format(conta_bl))
	print("x total de subjectes ADNIMERGE que tenen baseline visit pero tambe UN diagnostic a la baseline valid (no un na) {:.0f}".format(conta_bl_dxBL))
	

	#borro els  missings de ADNIMERGE del dicccionari de adni merge. I pregunto
	#si aquestos son a dic_valors_fMRI (i en cas que hi siguin els borro tambe)

	for subjecte_sense_DXBX_a_BaseLine in elimina_missings_diagnostics_ADNIMERGE:
		del dic_valors_amerge[subjecte_sense_DXBX_a_BaseLine]
		if subjecte_sense_DXBX_a_BaseLine in dic_subjectes_fMRIs:
			del dic_subjectes_fMRIs[subjecte_sense_DXBX_a_BaseLine]
		else:
			print("L'esborro de ADNIMERGE pero no de ARXIU FMRIS perque no hi es"+str(subjecte_sense_DXBX_a_BaseLine)) #'036_S_6189'
			#time.sleep(3)
	




	# PAS 2: busco subectes amb fMRI (o sigui, entre els que estan com a claus a 
	# dic_subjectes_fMRIs) que NO tenen registre al fitxer dinfo diagnostica (no son dins dic_valors_amerge).
	# els poso dins ll_ids_NOMES_fMRI.
	ll_ids_nomes_fMRI = []
	for clau in dic_subjectes_fMRIs:
		if not clau in dic_valors_amerge:
			ll_ids_nomes_fMRI = ll_ids_nomes_fMRI + [clau] 


	# PAS 3: Faig el mateix que al pas 2 però al revés. Busco, d'entre els que son dins el
	#fitxer d'info diagnostica (els que tenen clau dins dic_valors_amerge) quins d'ells
	# no tenen cap fMRI presa ()
	ll_ids_nomes_ADNIMERGE = []
	for clau in dic_valors_amerge:
		if not clau in dic_subjectes_fMRIs:
			ll_ids_nomes_ADNIMERGE = ll_ids_nomes_ADNIMERGE + [clau]
	

	print("DIAGRAMA_FLUX_subjectes que tenen info diagnostica (sona ADNIMERGE) pero no tenen CAP fMRI (no son a fitxer fMRI): {:.0f}".format(len(ll_ids_nomes_ADNIMERGE)))
	print("percentatge subjectes ADNI que tenen com a minim una fMRI: {:.0f}".format((len(dic_valors_amerge) - len(ll_ids_nomes_ADNIMERGE)) / len(dic_valors_amerge)))
	print("DIAGRAMA_FLUX_subjectes amb una fMRI com a minim, pero que NO TENEN info diagnostica perque no son al fitxer adnimerge: {:.0f}".format(len(ll_ids_nomes_fMRI)))
	
	#ESBORRO SUBJECTES DEL DIC FMRI QUE NO TENEN INFO DIAGNOSTICA
	i=0
	for subjecte_esborrar in ll_ids_nomes_fMRI: 
		del dic_subjectes_fMRIs[subjecte_esborrar]
		i = i + 1

	#ESBORRO SUBJECTES DEL DIC D'INFO DIAGNOSTICA (EL DE ADNIMERGE) QUE NO TENEN FMRIs
	for subjecte_esborrar in ll_ids_nomes_ADNIMERGE:
		del dic_valors_amerge[subjecte_esborrar]
			
		 
	print("DIAGRAMA_FLUX_Subjectes amb alguna fMRI I ALHORA info diagnostica: {:.0f}".format(len(dic_subjectes_fMRIs)))
	#time.sleep(1)
	
	#CORRECTE!!! ESTÀ PERFECTE. CORRESPONDÈNCIA BIJECTIVA.
	print(len(dic_valors_amerge.keys()) == len(dic_subjectes_fMRIs.keys()))
	print(len(dic_valors_amerge.keys()))

	#passo el diccionari amerge a llista
	ll_valors_amerge = [] #la faig buida! l'anterior es obsoleta
	for clau_subjecte in dic_valors_amerge:
		for linia_info_adnimerge in dic_valors_amerge[clau_subjecte]:
			ll_valors_amerge = ll_valors_amerge + [linia_info_adnimerge]
			
	#passo el diccionari fMRI a llista
	ll_valors_fMRI = [] #la faig buida! l'anterior es obsoleta
	for clau_subjecte in dic_subjectes_fMRIs:
		for linia_info_fMRI in dic_subjectes_fMRIs[clau_subjecte]:
			ll_valors_fMRI = ll_valors_fMRI + [linia_info_fMRI]		
	
	#passo la llista de nou al dataframe object. peto l'anterior i poso el nou depurat
	df_amerge = pd.DataFrame(data = ll_valors_amerge, columns = ll_capsalera_amerge)
	
	#passo la llista de nou al dataframe object.
	if len(ll_valors_fMRI[0]) == len(ll_capsalera_fMRIs):
		print("OKEY")
		#time.sleep(5)
	
	#passo la llista a pandas dataframe.
	
	df_fMRI = pd.DataFrame(data = ll_valors_fMRI, columns = ll_capsalera_fMRIs)

	
	
	print("\ntotal de 751 diagnostics baseline... tots els escanejates el tenen:")
	print(df_amerge["VISCODE"].value_counts())
	print("\nNO HI HA MISSINGS :):")
	print(df_amerge["DX.bl"].value_counts())	
	print("\nEvaluo quins diagnostics hi ha a la baseline (queda evaluar encara quins d'aquestos tenen fmri a la baseline")
	
	#	DX.bl  --> 1 "CN"| 2 "SMC"| 3 "EMCI" |4 "LMCI" |5 "MCI"| 6 "AD" 
	print(df_amerge[df_amerge["VISCODE"] == "bl"]["DX.bl"].value_counts())	
	print(df_amerge["VISCODE"].value_counts()) #MIRO COM DECAUEN ELS SUBJECTES (MIRAT DE ADNI MERGE)
	
	#MESOS EN QUE ES FAN LES VISITEs (llx)
	#(ORDENATS PER ORDRE CREIXENT DE LAALTRA VARIABLE (VALUECOUNTS))
	ll_x = "0,6,12,24,3,18,48,36,30,60,72,84,42,66,78,96,54,108,90,120,132,144,102".split(",")
	for i in range(len(ll_x)):
		ll_x[i] = int(ll_x[i])
	
	#AGAFO EL NOMBRE DE SUBJECTES QUE HI HA A CADA MES (CORRELATIU A LL_X 5 LINIES ENDARRERE)
	ll_y = list(df_amerge["VISCODE"].value_counts())
	
	#plt.plot(ll_x,ll_y,"ro")
	#plt.title("Participants scanned with fMRIs: Study drop out")
	#plt.ylabel("Number of participants")
	#plt.xlabel("visit (month)")
	#plt.show()
	
	#TOTS TENEN 751 SUBJECTES. DADES BEN FETES!
	print(len(dic_valors_amerge),len(dic_subjectes_fMRIs),len(list(df_amerge["PTID"].value_counts())),len(list(df_fMRI["Subject"].value_counts())))
	return dic_valors_amerge, dic_subjectes_fMRIs, df_amerge, df_fMRI, ll_capsalera_amerge

	
	#FILTRO PERSONES QUE TENEN MCI A BASELINE:
	# CODIS EMCI --> 3, LMCI --> 4 i, finalment, MCI --> 5
	#df_MCIs = df[(df["DX.bl"] == 3) | (df["DX.bl"] == 4) | (df["DX.bl"] == 5)]

def descriptius_diagrama_flux():
	""" Recorda
		#	DX.bl  --> 1 "CN"| 2 "SMC"| 3 "EMCI" |4 "LMCI" |5 "MCI"| 6 "AD" 
		
	"""
	dic_valors_amerge, dic_subjectes_fMRIs, df_amerge, df_fMRI = IMPORTANT_depura_ADNI_MERGE_i_ARXIU_fMRIs()
	
	print("#####################################################")
	#NOMBRE SUBJECTES A LA LINIA BASE PER CONDICIONS
	print(df_amerge[df_amerge["VISCODE"] == "bl"]["DX.bl"].value_counts())
	print("#####################################################")
	
	#PAS 1:              
   #dic_valors_amerge --> EXAMDATE ('aaaa-mm-dd') ---> (posició 6 en llista-valor)
	#dic_subjectes_fMRIs --> Acq Date ('mm/dd/aaaa') --> (posicio 9 en llista-valor) 
	print("AMERGE: ",dic_valors_amerge["123_S_6118"][0][6])
	print("FMRI: ",dic_subjectes_fMRIs["123_S_6118"][0][9])
	print("les MODALITATS DE fMRI i el nombre de les mateixes: ")
	
	#AQUI POTS VEURE LES DIFERENTS MODALITATS DE fMRI utilitzades 
	print(df_fMRI["Description"].value_counts())
		


#descriptius_diagrama_flux()


def ajusta_data(data):
	"""pilla data format 'aaaa-mm-dd' (de l'adnimerge) i retorna data format 'mm/dd/aaaa'"""
	data = data.split("-"); data.reverse()
	swap = data[0]; data[0]=data[1]; data[1] = swap
	return "/".join(data)



def busca_MCI_a_SA(ll_diag_persona, ll_EMCI_A_SA, ll_LMCI_A_SA):
	DXbl = ll_diag_persona[0][2][0] #només el carrego un cop pq l'informacó guardeada es redundant
	if DXbl == 3: #EMCI a baseline
		for i in range(len(ll_diag_persona)): #recorda, llista ordenada
			ll_EMCI_A_SA += [ll_diag_persona[i][2][1]] #el diagnostic de la screening visit
	elif DXbl == 4: #LMCI a baseline
		for i in range(len(ll_diag_persona)): #recorda, llista ordenada
			ll_LMCI_A_SA += [ll_diag_persona[i][2][1]] #el diagnostic de la screening visit
	return ll_EMCI_A_SA, ll_LMCI_A_SA
					

def imprimeixTXT_filtre_SPSS_metodes(ll_claus_blocprovisional):
	"""funcio per a filtrar els 184 emcis i els 148 LMCIs a l'spss. Veure diagrama de flux nodes inmediatament abans de lo verd"""
	with open("input_COLUMNA_ID_copiada_INTACTA_DE_ADNIMERGE.txt","r") as f_in:
		with open("output_variable_filtre_spss_INCLOSOS_apartat_metodes.txt","w") as f_out:
			for id_linia in f_in:
				if id_linia[:-1] in ll_claus_blocprovisional:
					f_out.write(str(1)+'\n')
				else:
					f_out.write(str(0)+'\n')
				

def perburrorepeteixocodi(clau_subjecte, dic_valors_amerge):
	"""
	busco l'exam date per a la la linia base d'un subjecte
	i el retorno formatejat en el formateig original aaaa-mm-dd. 
	També busco l'RID corresponent per despres dir si es ADNI3 o ADNI2.
	
	Els RID corresponents a l'ADNI3 no els trobava. La dada utilitzada aquí
	s'ha obtingut a partir de la pregunta que vaig fer al forum de l'adni (RID >= 6000 --> adni3):
		
	https://groups.google.com/forum/#!topic/adni-data/VuIEUSUcl_M
	"""
	
	ll_dades_subjecte = dic_valors_amerge[clau_subjecte] #faig copia de la info fenotipica per a cada subjecte, per no petar res
	for linia_examen in ll_dades_subjecte:
		examdate = linia_examen[6] #la funcio passa de aaaa-mm-dd a dd/mm/aaaa. Ojo, pq em complico la vida despres, pero es igual pq ho vull veure en català 
		viscode = linia_examen[5]
		RID = linia_examen[0]
		if viscode =="bl":
			if RID <  2000:
				fase_estudi = "ADNI_1"
			elif 2000 <= RID < 4000:
				fase_estudi = "ADNI_GO"
			elif 4000 <= RID < 6000:
				fase_estudi = "ADNI_2"
			else: #tal que RID >= 6000 --> ADNI:3 --> https://groups.google.com/forum/#!topic/adni-data/VuIEUSUcl_M
				fase_estudi = "ADNI_3"
			return examdate, RID, fase_estudi #esquema de cerca
		



def data_menysdies_i_de_nou_a_data(data_dxbl,dif_esc_dxbl):
	"""
	pilla data dxbl en format natural adnimerge (aaaa-mm-dd) i en torna una altra
	de (aaaa-mm-dd) que es quan es va fer l'escaner. Per a fer-ho Prenem el vector diferència acq date de l'escaner + diferencia (positiva o negativa)
	en relacio a data dxbl.
	Obtenim la data d'adquisició de l'escàner amb la qual bàsicament 
	"""
	
	data_dxbl = data_dxbl.split("-")
	anny, mes, dia = int(data_dxbl[0]),int(data_dxbl[1]),int(data_dxbl[2])
	data_dxbl = datetime.datetime(anny,mes,dia) + datetime.timedelta(int(dif_esc_dxbl))
	return data_dxbl.strftime("%Y-%m-%d %H:%M:%S").split()[0] #GRACIES <3 https://stackoverflow.com/questions/7999935/python-datetime-to-string-without-microsecond-component
	
#print(data_menysdies_i_de_nou_a_data("2012-05-19",-6))

def fes_taula_metodes(ll_conteig, ll_centres):
	"""
	TAULA LATEX ANNEX. CENTRES ADNI despres "entry criteria"
	"""
	ll=[]
	for i in range(len(ll_conteig)):
		ll += [[ll_conteig[i],ll_centres[i]]]
	print(ll)
	ll.sort() #ORDENO
	ll.reverse() #ORDENO DECREIXENT
	with open("taula_metodes.txt","w") as f:
		f.write("Number of subjects assessed & Center code number & Center name \\\  "+"\n") #PQ ES MENJA UNA CONTRABARRA?
		for i in range(len(ll)):
			f.write(str(ll[i][0])+" & "+str(ll[i][1])+" &  \\\   "+"\n")
			 
		




def temps_de_conversio(SUBMODALITAT_fMRI):
	""" 
	
	INPUT (str): Modalitat per a la qual vols obtenir l'excel resum 
	
			#'relCBF'                                             
			#'MoCoSeries'                                        
			#'ASL PERFUSION' |'ASL_PERFUSION'|'ASL'|'ASL PERF'    (CALDRIA MIRAR COM AJUNTARHO)
			# 'Resting State fMRI'   -sudo de eyes open-           
	
			###################################################### N subjectes per submodalitat (TOTAL GRUPS) - CAL DESCONTAR ELS QUE TENEN DUPLICITATS PERQUE QUQADRI EL CALCUL 
		
	
	 "MoCoSeries"
	
	Aquest script és molt important. En essència el que fa és mirar qui es conver
	teix a AD. I et diu quants dies tarda des de que aquest rep el diagnostic de la Baseline,
	que és el diagnostic més certer, a convertir-se a AD. 
	
	
	També cerca l'escàner més proper a la baseline per a la modalitat demanada al paràmetre de la funcio. I treu un .csv amb les variables:
	BL.dx	| s_CONVER	| CLAU	| DIES-SEGUIM	| submod_fmri	| data_dxbl	 | dif_examdate_vs_dxbl	| data_escaneig |	scans_mateixdia
	
	Que de forma respectiva son:
		
	- diag linia base
	- si es torna AD o no en el futur (només si hi ha un seguiment ja s'inclou! Caldrà fer un tall per temps mínim de seguiment)
	- DIES-SEGUIM --> Si la persona es torna alzheimer (CLAU=1) aquest adada son dies que tarda persona a tornar-se AD des de l'establiment de la linia base.
	- 
	
	# DX.bl  --> 1 "CN"| 2 "SMC"| 3 "EMCI" |4 "LMCI" |5 "MCI"| 6 "AD" 
	# DX ------> 1 "CN" | 2 "MCI" | 3 "AD" --> TRET DE LA MANIGA PERO CREC QUE ESTA B
	"""

	dic_valors_amerge, dic_subjectes_fMRIs, df_amerge, df_fMRI, ll_capsalera_amerge = IMPORTANT_depura_ADNI_MERGE_i_ARXIU_fMRIs()
	#SUBJECTE MOSTRA ENVIAT
	#print(df_amerge[df_amerge["PTID"]=="053_S_4813"])
	#print(df_fMRI[df_fMRI["Subject"]=="053_S_4813"])
	#return
	####


	#BUSCO LES CONVERSIONS PER PATOLOGIA (si converteix a AD, no no converteix): Combinaciones explorables pero no explorades  #CN_a_AD = {"si" : [], "no":[]}   #SMC_a_AD = {"si": [], "no" : []} 
	#AL PRIMER ELEMENT DE LA LLISTA POSEM ELS QUE SÍ I AL SEGON ELS QUE NO 
	EMCI_a_AD = {'si':[], 'no':[]} #{"SI" : [[ID_1,DIES_CONVERSIO_1],[ID_2,DIES_CONVERSIO_2], ...,], "NO": [[ID_1,DIES_SEGUIMENT_SENSECONVERSIO_1],[ID_1,DIES_SEGUIMENT_SENSECONVERSIO_1]]
	LMCI_a_AD = {'si':[], 'no':[]}
	MCI_a_AD =  {'si':[], 'no':[]}
	j=0
	k=0
	l=0
	
	EMCI_a_AD_SENSESEGUIMENTS = [] #subjectes EMCI que no tenen cap seguiment i que s'han esborrat (CONSTÀNCIA PER AL FLOW DIAGRAM, SIMPLEMENT)
	LMCI_a_AD_SENSESEGUIMENTS = [] #subjectes LMCI que no tenen cap seguiment i que s'han esborrat 
	
	dic_aux_dates_baselines = {} #dict que guardara {"idsubecte" : "data baseline", per a tots els subjectes de dic_a_mergeand so on}. L'usare després per creuar els dos fitxers (ADNI merge i fmris)
	
	#busco els EMCI o LMCI diagnosticats com a tal a BL, que en algun moment en el futur reben el diagnostic de sans
	ll_EMCI_A_SA = []
	ll_LMCI_A_SA = []
	
	
	for clau_subjecte in dic_valors_amerge:
		ll_dades_subjecte = dic_valors_amerge[clau_subjecte] #faig copia de la info fenotipica per a cada subjecte, per no petar res

		
		ll_dates = []
		ll_diagnostics = []
		for linia_examen in ll_dades_subjecte:
			ll_dates += [ajusta_data(linia_examen[6])] #PILLO EXAMDATE, AMB FORMATEIG AJUSTAT --> ['10/24/2005', '04/24/2006', '11/01/2006', '04/24/2007', '10/31/2007', '05/16/2008', '10/22/2008', '10/07/2010', '04/28/2011', '10/10/2011', '04/02/2012', '10/03/2012', '04/18/2013', '10/10/2013', '04/15/2014', '10/27/2015', '11/27/2017']
			ll_diagnostics +=  [(linia_examen[7],linia_examen[59])] #AGAFO DX.bl i DX
		ll_dates_vectoritzades = Dates(ll_dates[:]).vectoritza_dates() #POSO DATES EN FORMA VECTOR (DIA 0 PER A LA DATA MES PETITA (DIA DIAGNOSTIC BASELINE), I LA RESTA DIES DES DE LA BASELINE. S'HAGUES POGUT FER AMB LA VARIABLE M (la ultima de ADNIMERGE... pero no ho vaig veure i em vaig complicar la vida xDD, però el resultat ens duu al mateix, però amb més precisió))
		for i in range(len(ll_dates_vectoritzades)):
			ll_dates[i] = [ll_dates_vectoritzades[i],ll_dates[i],ll_diagnostics[i]]
		ll_dates.sort()
		ll_diag_persona = ll_dates; del ll_dates; del ll_diagnostics
		dic_aux_dates_baselines[clau_subjecte] = ll_diag_persona[0][1]

		#      ARA ll_diag_persona PREN LA SEGUENT ESTRUCTURA:
		#  una llista on a subllistes tens cada VISITA, ordenada de forma ascendent per data segons:
		#  [[vector_dies**, EXAM_DATE, (DX.bl,DX)], [],[],...,[]]] --> **dies_respecte_lorigen (respecte baseline)
		#  [[0, '10/24/2005', (1.0, 1.0)], 
		#   [182, '04/24/2006', (1.0, 1.0)], 
		#   [373, '11/01/2006', (1.0, 1.0)], 
		#   [... ]]

		
		ll_EMCI_A_SA, ll_LMCI_A_SA = busca_MCI_a_SA(ll_diag_persona, ll_EMCI_A_SA, ll_LMCI_A_SA)  #MIRO A MES QUINS SON PROBLEMATICS (EMCIS O LMCIS DIAGNOSTICAS ACOM A TAL A BL QUE, ES ESTRANY, REBEN DESPRES EL DIAGNOSTIC DE SA)
		
		
		
		#ARA CLASSIFIQUEM CADA SUBJECTE EN CADA CATEGORIA
		DXbl = ll_diag_persona[0][2][0] #només el carrego un cop pq l'informacó guardeada es redundant
		CONVERTIT = False
		if not DXbl == 6: #Si ja té alzheimer a la BL ja no cal mirar si es convertirà a alzheimer xD	
			if DXbl == 3: #EMCI a baseline
				j=j+1
				
				for i in range(len(ll_diag_persona)): #recorda, llista ordenada
					DX = ll_diag_persona[i][2][1] #el diagnostic de la screening visit
					dies_desde_bl, DX = ll_diag_persona[i][0], ll_diag_persona[i][2][1]
					if DX == 3: #DIAGNOSTIC D'ALZHEIMER A LA VISITA DONADA 					
						EMCI_a_AD['si'] += [[clau_subjecte, dies_desde_bl]] #GUARDO CLAU SUBJECTE I DIA EN QUE FEM DIAGNÒSTIC DE CONVERSIO (DIA EN QUE CONVERTEIX, I MES DES DE LA BASELINE EN EQUE CONVERTEIX)
						CONVERTIT = True
						#COMPROVO
						if len(ll_diag_persona)<=1:
							print("PROBLEMA DE DIAG BASELINE!!")
							print(len(ll_diag_persona)) 
						break #JA SABEM QUE S'HA CONVERTIT, SORTIM DEL FOR. MILLORA AMB SCRIPT DEEVALUAR CONSISTENCIA POSTERIORS DIAGNOSTICS												
				if not CONVERTIT: #SI ARRIBO AL FINAL I NO HE TROBAT CONVERSIÓ POSO QUE NO S'HA CONVERTIT.
					if i==0: #CAS EN QUE LA PERSONA EN CONCRET NO TÉ CAP SEGUIMENT!! NO ENS SERVEIX. NOMES EL GUARDEM PER REPORTAR-LO
						EMCI_a_AD_SENSESEGUIMENTS += [clau_subjecte] #
					else: #cas i>0
						EMCI_a_AD['no'] +=[[clau_subjecte, dies_desde_bl]]


					
			elif DXbl == 4: #LMCI a baseline
				k=k+1
				for i in range(len(ll_diag_persona)): #recorda, llista ordenada
					DX = ll_diag_persona[i][2][1] #el diagnostic de la screening visit
					dies_desde_bl, DX = ll_diag_persona[i][0], ll_diag_persona[i][2][1]
					if DX == 3: #DIAGNOSTIC D'ALZHEIMER A LA VISITA DONADA
						LMCI_a_AD['si'] += [[clau_subjecte, dies_desde_bl]] #GUARDO CLAU SUBJECTE I DIA EN QUE FEM DIAGNÒSTIC DE CONVERSIO (DIA EN QUE CONVERTEIX, I MES DES DE LA BASELINE EN EQUE CONVERTEIX)
						CONVERTIT = True
						if len(ll_diag_persona)<=1:
							time.sleep(10)
							print("PROBLEMA DE DIAG BASELINE!!")
							print(len(ll_diag_persona))
							return
						break #JA SABEM QUE S'HA CONVERTIT, SORTIM DEL FOR. MILLORA AMB SCRIPT DEEVALUAR CONSISTENCIA POSTERIORS DIAGNOSTICS												
				if not CONVERTIT: #SI ARRIBO AL FINAL I NO HE TROBAT CONVERSIÓ POSO QUE NO S'HA CONVERTIT.
					if i==0: #CAS EN QUE LA PERSONA EN CONCRET NO TÉ CAP SEGUIMENT!! NO ENS SERVEIX. NOMES EL GUARDEM PER REPORTAR-LO
						LMCI_a_AD_SENSESEGUIMENTS += [clau_subjecte] #
					else: #cas i>0
						LMCI_a_AD['no'] +=[[clau_subjecte, dies_desde_bl]]

			elif DXbl == 5: #MCI a baseline
				l=l+1
				for i in range(len(ll_diag_persona)): #recorda, llista ordenada
					DX = ll_diag_persona[i][2][1] #el diagnostic de la screening visit
					dies_desde_bl, DX = ll_diag_persona[i][0], ll_diag_persona[i][2][1]
					if DX == 3: #DIAGNOSTIC D'ALZHEIMER A LA VISITA DONADA
						MCI_a_AD['si'] += [[clau_subjecte, dies_desde_bl]] #GUARDO CLAU SUBJECTE I DIA EN QUE FEM DIAGNÒSTIC DE CONVERSIO (DIA EN QUE CONVERTEIX, I MES DES DE LA BASELINE EN EQUE CONVERTEIX)
						CONVERTIT = True
						print("PROBLEMA DE DIAG BASELINE!!")		
						time.sleep(10)
						break #JA SABEM QUE S'HA CONVERTIT, SORTIM DEL FOR. MILLORA AMB SCRIPT DEEVALUAR CONSISTENCIA POSTERIORS DIAGNOSTICS												
				if not CONVERTIT: #SI ARRIBO AL FINAL I NO HE TROBAT CONVERSIÓ POSO QUE NO S'HA CONVERTIT.
					MCI_a_AD['no'] +=[[clau_subjecte, dies_desde_bl]]
			else: 
				pass#PODRIES MIRAR, PER CURIOSITAT, QUÈ PASSA AMB ELS SMC (QUE NO SE QUI CONY SON) I ELS CN
		else:
			pass
		

	
	df_EMCI_estornaSA = pd.DataFrame(data={"a":list(range(len(ll_EMCI_A_SA))),"EMCI_A_ALGO": ll_EMCI_A_SA})
	df_LMCI_estornaSA = pd.DataFrame(data={"b":list(range(len(ll_LMCI_A_SA))),"LMCI_A_ALGO": ll_LMCI_A_SA})
	
	
	print(df_EMCI_estornaSA["EMCI_A_ALGO"].value_counts())
	print(df_LMCI_estornaSA["LMCI_A_ALGO"].value_counts())
	
	#continua per aqui
	
	
	#VOLCAHO! http://adni.loni.usc.edu/study-design/background-rationale/	
	print("\nWe excluded the following subjects due to not having (12 of them) any screening visit and one of them for not having baseline visit and only one screening visit. Besides, the MCI diagnostic was deprecated in ADNI go/2, only common to ADNI 1 (where there were no fMRIs!)")
	print(MCI_a_AD["no"],"\nTOTAL EMCIS amb alguna fMRI: "+str(j), "\nTOTAL LMCIS amb alguna fMRI: "+str(k),"\nTOTAL MCIs amb fMRI: "+str(l))
	


	#dic_valors_amerge[clau_subjecte] += 	
	#POSA QUE ELS EXCLOUS DE LA MOSTRA FINAL  (son els MCIs)
	#AL DIAGRAMA FINAL [['027_S_6002', 361], ['941_S_6017', 0], ['024_S_6033', 0], 
	# ['027_S_6034', 0], ['141_S_6041', 0], ['130_S_6047', 0], ['941_S_6052', 0], 
	# ['301_S_6056', 0], ['941_S_6068', 0], ['141_S_6075', 0], ['037_S_6083', 0], 
	# ['135_S_6110', 0], ['037_S_6125', 0]] 





	#ARA MIRO QUANT DE TEMPS DE SEGUIMENT HI HA PER ALS SUBJECTES QUE NO PASSEN
	# DE EMCI A LMCI. HEM D'ESTABLIR UN UMBRAL MÍNIM DE SEGUIMENT. 
	
	ll_dies_no_conver_EMCI = []
	claus_subjectes_no_converters_EMCI = []
	for sub in EMCI_a_AD["no"]: #[[027_s_6969, 45],[024_S_3333, 96]] [CLAU, DIES BASELINE]
		ll_dies_no_conver_EMCI += [sub[1]]
		claus_subjectes_no_converters_EMCI += [sub[0]]
	print("DIES DE SEGUIMENT MÀXIMS PER ALS QUE NO ES CONVERTEIXEN DE [ EMCI ] A AD")
	print(ll_dies_no_conver_EMCI)

	
	ll_dies_no_conver_LMCI = []
	claus_subjectes_no_converters_LMCI = []
	for sub in LMCI_a_AD["no"]: #[[027_s_6969, 45],[024_S_3333, 96]] [CLAU, DIES BASELINE]
		ll_dies_no_conver_LMCI += [sub[1]]
		claus_subjectes_no_converters_LMCI += [sub[0]]

	print("\nDIES DE SEGUIMENT MÀXIMS PER ALS QUE NO ES CONVERTEIXEN DE [ LMCI ] A AD")
	print(ll_dies_no_conver_LMCI)
	
	# DATAFRAMES QUE CONTENEN ELS DIES DE SEGUIMENT DELS SUBJECTES EMCI I LMCI (RESPECTIVAMENT) QUE 
	# NO (REPETEIXO, NO) ES CONVERTIRAN. SERVEIXEN PER VEURE SI HI HA PROU TEMPS DE NO CONVERSIO
	# COM PER DIR QUE SON PACIENTS QUE NO EVLUCIONARÀN PAS A ALZHEIMER
	
	df_seg_EMCI = pd.DataFrame(data = {"id" : claus_subjectes_no_converters_EMCI, "dies_seg" : ll_dies_no_conver_EMCI})
	df_seg_LMCI = pd.DataFrame(data = {"id" : claus_subjectes_no_converters_LMCI, "dies_seg" : ll_dies_no_conver_LMCI})
	




	print(df_seg_EMCI)
	print(df_seg_LMCI)
	#ELS EMCI i LMCI que no tenen cap FOLLOW-UP (evidentment no els inclourem als analisis).
	# aquestos es troben en aquelles persones EMCI O LMCI per a les qualS NO HEM TROBAT PAS
	# una conversio a alzheimer.
	print("\nEMCIS que no tenen CAP seguiment -JA EXCLOSOS- (n = -"+str(len(EMCI_a_AD_SENSESEGUIMENTS))+")")
	print(EMCI_a_AD_SENSESEGUIMENTS)
	
	print("\nLMCIS que no tenen CAP seguiment -JA EXCLOSOS- (n = -"+str(len(LMCI_a_AD_SENSESEGUIMENTS))+")")
	print(LMCI_a_AD_SENSESEGUIMENTS)



	
	dic_tipus_escaners_a_baseline =  {} #aquí hi guardarem els escaners a la baseline
	cont = 0
	
	
	#SI VOLS VEURE EL NOMBRE D'ESCANERS QUE HI HA PER CADA SUBGRUP, TREU EL PRIMER FOR
	#I EN COMPTES DE FOR ID_SUBJECTE,DIES_CONVERSIO IN GRUP, CANVIAHO PER
	# FOR ID_SUBJECTE_DIES_CONVERSIO IN EMCI_A_AD["SI"] O QUALSEVOL DE LES
	# ALTRES 3 OPCIONS DINS MCI
	
	stack_ll_dies = [] #PER A FER EL CSV
	stack_ll_modal = [] # PER A FER EL CSV
	
	
	
	
	
	ll_MCI = [EMCI_a_AD["si"], LMCI_a_AD["si"], EMCI_a_AD["no"], LMCI_a_AD["no"]]
	for grup in ll_MCI:
		for id_subjecte, dies_conversio in grup:
			ll_acq_date = []
			ll_tipus_fmri = []
			for sessio_neuroimatge in dic_subjectes_fMRIs[id_subjecte]:
				ll_acq_date += [sessio_neuroimatge[9]] # POSO DATES D'AQDQUISICIO A LLISTA PER TREURE VECTOR
				ll_tipus_fmri += [sessio_neuroimatge[7]] # POSO DATES
			
			# IMPORTANTISSIM: AFEGEIXO AL primer element de la llista de ll_acq_date 
			# (que conté les dates de les fMRI vectoritzades en dies) la data en que es fa el DX.bl 
			# (provinent de adnimerge)
			ll_acq_date = [dic_aux_dates_baselines[id_subjecte]] + ll_acq_date
			
			#PER A ANIVELLAR L'ESPAI QUE HEM AFEGIT ABANS POSEM UN ESTPAI ANIVELLADOR  perquè no hi hagi problemes despres en indexar entre ll_acq_date i ll_tipus_fmri
			ll_tipus_fmri = ["espaiAnivellador"] + ll_tipus_fmri
			vector_acq_date = Dates(ll_acq_date).vectoritza_dates() 
			
			#[DX_BL, DIES ESCANER, DIES ESCANER... ETC]
			#[0, 1499, 1499, 1499, ....],[0, 1464, 1464, 1464, 1464, 1088, 1088...]]
			
			# OJO: L'ORIGEN DE LA LLISTA VECTORITZADA DE DIES HA D'ANAR EN RELACIÓ AL MOMENT DEL BL.DX
			# NO PAS EN RELACIÓ A LA PRIMERA FMRI PRESA (PODRIA SER UNA FMRI PRESA 2 MESOS ABANS DE LA DX.BL PER EXEMPLE.
			# PER TANT RESTO CADA UN DELS VALORS DE LA LLISTA PEL NOMBRE DE DIES QUE TÉ LA DX BL,
			# AIXI L'ORIGEN DEL SISTEMA DE COORDENADES (MOMENT DE PRESA DX.BL DE ADNIMERGE) 
			# QUEDA FIXAT EN EL 0
			 
			blDX_origen = vector_acq_date[0]
			for i in range(len(vector_acq_date)):
				 vector_acq_date[i] = vector_acq_date[i] - blDX_origen
			
			#ARA CERCO ELS ESCANERS MES PROPERS A LA BASELINE PER CADA SUBJECTE I EN MIRO ELS TIPUS
			# AMB EL MODEL DE CLASSIFICACIO HEM DE FER-NE SERVIR NOMÉS UN, NO?
			cop_fmri = ll_tipus_fmri[:][1:] 
			cop_acq = vector_acq_date[:][1:]
			##################################################
			#DEFINEIXO UNA SERIE NUMÈRICA PER CERCAR ELS ESCANERS CORRESPONENTS AL DIA MES PROPER A LA BASELINE
			#################################################
			val_min = min(cop_acq, key=abs) #prenc el dia minim. Si cop_acq fos = [23,-12,300,13] --> torna -12
			x = val_min
			ll_dies = [] # conté dies que fa que s'ha pres la fmri des de la baseline per a un subjecte donat
			ll_modal = []# conté modalitat fmri
			j = 0
			while x == val_min: #deixo de buscar un cop ja he trobat totes les fMRIs registrades al primer dia
				i = cop_acq.index(x) #busco index i de l'escaner més proper a la baseline
				ll_dies += [cop_acq[i]] #afegeixo diferencia de dies a lal lista dies
				ll_modal += [cop_fmri[i]] #afegeixo diferencia de fmris a la llista de fmris
				dic_tipus_escaners_a_baseline = posa_a_dict_2(cop_fmri[i],dic_tipus_escaners_a_baseline)
				del cop_fmri[i]
				del cop_acq[i]
				try:
					x = min(cop_acq, key=abs)
				except ValueError:
					break #quan un subjecte només té escaners presos en un dia (i cap altre escaner) la llista es quedaria buida i donaria error 
	
			print(id_subjecte) 
			print(ll_dies)
			print(ll_modal)
			
			#EMMAGATZEMEM ELS DIES I LES MODALITATS PER CADA SUBJECTE EN 
			#SEGNLES LLISTES. P EX.
			

			
			#141_S_0915
			#[2570, 2570, 2570, 2570]
			#['ASL PERFUSION', 'relCBF', 'MoCoSeries', 'Perfusion_Weighted']
				
			#137_S_4816
			#[-24, -24, -24, -24]
			#['ASL_PERFUSION', 'Perfusion_Weighted', 'relCBF', 'MoCoSeries']
			
			#quedara ordenat sense id:
			

			#stack_ll_dies=[[570, 2570, 2570, 2570],[[-24, -24, -24, -24]]
			#stack_ll_modal=[['ASL PERFUSION', 'relCBF', 'MoCoSeries', 'Perfusion_Weighted'],['ASL_PERFUSION', 'Perfusion_Weighted', 'relCBF', 'MoCoSeries']]
			
			#I AIXO SERVIRA PER A FER EL .CSV DE ADNIMERGE_linqueja_amb_fmri.csv
			
			
			stack_ll_dies += [ll_dies]
			stack_ll_modal += [ll_modal]
			cont += 1
			print("")

	print("#####################################")
	print(str(cont)+" subjectes avaluats.")   
	print("#####################################")   
	print("\n")
	print("Nombre d'escaners per tipus, dins d'aquests"+str(cont)+" subjectes avaluats:")
	print("Nota: MoCoSeries et surt 192 si t'hi fixes... pero aixo es el total d'escaners que han rebut els subjectes el dia mes proper a la baseline\n, no pas el total de subjectes amb MCI (EMCI, LMCI) que hi ha. Bàsicament hi ha 5 subjectes que reben dos escaners MoCo el mateix dia, i per aixo si vols obtenir els MoCo en el fitxer separat te'n surten 187 (192 - 5 = 187).")
	print(dic_tipus_escaners_a_baseline)
	
	#MOSTRA EL NOMBRE DE SUBJECTES QUE HI HA SOTA ELS NODES VERDS DEL DIAGRAMA DE FLUX
	a,b,c,d = len(EMCI_a_AD["si"]), len(EMCI_a_AD["no"]), len(LMCI_a_AD["si"]), len(LMCI_a_AD["no"])
	print("\nMOSTRA PER AL FLOW DIAGRAM DESPRES DE CRITERIS D'EXCLUSIO")
	print('EMCI_a_AD["si"]: {:.0f}\nEMCI_a_AD["no"]: {:.0f}\nLMCI_a_AD["si"]: {:.0f}\nLMCI_a_AD["no"]: {:.0f}'.format(a,b,c,d))
	
	
	#CREEEM UNA NOVA VARIABLE [CONVERSIO]. A PARTIR DAQUI HO HAURAS DE MODIFICAR O POTSER BORRAR PER 
	#ESTRATIFICAR PER SIMPLEMENT MALALTIA O B89E 
	ll_MCI = [EMCI_a_AD["si"], LMCI_a_AD["si"], EMCI_a_AD["no"], LMCI_a_AD["no"]]
	codifica_conversio = [1,1,0,0]
	codis_bldx = [3,4,3,4] #RECORDA, 3 per a EMCI i 4 per a LMCI
	#print(df_amerge)
	
	#ESCRIVIM ELS PARTICIPANTS EN UN CSV QUE ANIRA A SPSS.  ESTRUCTURA VARIABLES
	#CONVERSIO (1 = SI, 0 = NO) | CLAU SUBJECTE | TEMPS SEGUIMENT DES DE LA BASELINE DX [MESURA TEMPS FINS A QUE DETECTA CONVERSiO, ES A D IR QUAN TROBA DX VAL CODI DEMENCIA I FA BREAK, -SI CLAU SUBJECTE = 0-, O PER FALTA DE SEGUIMENTS] 
	#CREEM NOVES VARIABLES.
	conta = 0
	d_centres = {}
	ll_claus_blocprovisional = []
	
	

		
	#FAIG UN FITXER PER VEURE LA DISTRIBUCIÓ DELS SUBJECTES DESPRÉS DELS ENTRY CRITERIA (D'AQUEST
	# FITXER EN SURT LA DISTRIBUCIÓ DE DADES POSADA A LA INTRO
	with open("ADNIMERGE_sortida.csv","w") as f:
		f.write("BL.dx,s_CONVER,CLAU,DIES-SEGUIM\n") 
		for i in range(len(ll_MCI)):
			for j in range(len(ll_MCI[i])):
				 clau_subjecte, temps_seguiment = ll_MCI[i][j][0], ll_MCI[i][j][1]
				 d_centres = posa_a_dict_2(clau_subjecte.split("_")[0],d_centres) #PILLO NOMES ELS CODIS DE CENTRES I CONTO QUANTS SUBJECTE SHI HA PER CADA CODI DE CENTRE 
				 ll_claus_blocprovisional += [clau_subjecte]
				 f.write(str(codis_bldx[i])+","+str(codifica_conversio[i])+","+clau_subjecte+","+str(temps_seguiment)+'\n')
				 conta = conta + 1	
	print("REALMENT HE IMPRES UN PER PERSONA? --> ",conta == a+b+c+d)
	
	print("\ndiccionari CODI_CENTRE : SUBJECTES PER CENTRE")
	print("")
	print(d)
	fes_taula_metodes(list(d_centres.values()),list(d_centres.keys()))
	
	#FAIG UN SEGON FITXER ON AMPLIO EL FITXER ANTERIOR AMB LES SUBMODALITATS CORRESPONENTS
	#I LES VARIABLES QUE VOLDREM EVALUAR
	
	# a SUBMODALITAT_fMRI nomes has de triar una SUBMODALITAT. RECORDA QUE LES QUE MAXIMITZEN
	# EL NOMBRE DE SUBJECTES AMB ESCANER MES PROPER A BASELINE SON A PRIORI:
	# relCBF, MoCO series i ASL perfusion. Resting state es el que menys
	# però és el que escollirem aquí perquè a la upf saben preprocessar 
	# aquestes dades i me'n poden ensenyar.
	
	# IDENTIFICADORS PER A OBTENIR EL SUBCONJUNT de fMRI DESITJAT (subconjunts S1 fins a S4).
	
	#Aquests ids es fan servir per cercar a dins les carpetes!
	#l'etiquetatge es una mica patètic en alguna de les modalitats
	#en aquelles caldria fer servir tots els descriptors (concatenals amb OR)
	#i caldria canviar el codi.
	#EL NOM CORRESPONENT A LA VARIABLE submod_fmri):

		###################################################### N subjectes per submodalitat (TOTAL GRUPS) - CAL DESCONTAR ELS QUE TENEN DUPLICITATS PERQUE QUQADRI EL CALCUL 
	#S1 'relCBF'                                             191
	#S2 'MoCoSeries'                                         192
	#S3 'ASL PERFUSION' |'ASL_PERFUSION'|'ASL'|'ASL PERF'    141,23,7,9 respectivament --> CALDRIA MIRAR COM AJUNTARLOS
	#S4 'Resting State fMRI'   -sudo de eyes open-           103
		######################################################
		
	
	#NOTA QUE STACK_LL_MODAL I STAck_ll_dies van en tàndem
	
	k = 0 #index per recorrer stack_ll_dies i stack_ll_modal
	with open("ADNIMERGE_linqueja_amb_fmri.csv","w") as f:
		NOM_SUBMOD_FMRI_BUSCADA = SUBMODALITAT_fMRI    #MIRA LES LINIES ANTERIORS
		# rid el posem perque ens diu si pertany a ADNI2 o ADNI3. Si pertany a ADNI 3 aleshores les dades tenen un preprocessat
		# concret. En cas contrari, tenen un preprocessat... de moment incert.
		f.write("BL.dx,s_CONVER,PTID,DIES-SEGUIM,submod_fmri,data_dxbl,dif_examdate_vs_dxbl,data_escaneig,scans_mateixdia,rid,fase_estudi\n") 
		for i in range(len(ll_MCI)): #ITERO EN ELS 4 GRUPS DEFINITS 
			for j in range(len(ll_MCI[i])): #ITERO DINS CADA GRUP
				clau_subjecte, temps_seguiment = ll_MCI[i][j][0], ll_MCI[i][j][1]
				d_centres = posa_a_dict_2(clau_subjecte.split("_")[0],d_centres) #PILLO NOMES ELS CODIS DE CENTRES I CONTO QUANTS SUBJECTE SHI HA PER CADA CODI DE CENTRE 
				ll_claus_blocprovisional += [clau_subjecte]
				data_dxbl, RID, fase_estudi = perburrorepeteixocodi(clau_subjecte, dic_valors_amerge)
				dif_examdate_vs_dxbl = stack_ll_dies[k] #examdate dia de lescaner. dxbl linia base. aquesta variable en recull la dif

				for l in range(len(stack_ll_modal[k])): #RECORRO ALGO AIXI, COM LO DEL 020_S_4920 --> ['ASL_PERFUSION', 'MoCoSeries', 'Perfusion_Weighted', 'relCBF']
					scan = stack_ll_modal[k][l]
					if scan == NOM_SUBMOD_FMRI_BUSCADA:
						nre_escaners_mateixasubmodalitat_mateixdia = stack_ll_modal[k].count(NOM_SUBMOD_FMRI_BUSCADA) #L'ADNI INCORPORA UN SISTEMA DE QUALITAT. CREC QUE L'ESCANER SI SURT MALAMENT ES REPETEI EL MATEIX DIA. PER TANT HAURIES DE PRENDRE EL MES RECENT, AMB QUESTIO DE MINUTS:
						f.write(str(codis_bldx[i])+","+str(codifica_conversio[i])+","+clau_subjecte+","+str(temps_seguiment)+","+NOM_SUBMOD_FMRI_BUSCADA+","+data_dxbl+","+str(dif_examdate_vs_dxbl[l])+","+data_menysdies_i_de_nou_a_data(data_dxbl,str(dif_examdate_vs_dxbl[l]))+","+str(nre_escaners_mateixasubmodalitat_mateixdia)+","+str(RID)+","+fase_estudi+'\n')	
						break
				else:
					pass #SI ELS SUBECTES NO TENEN LA SUBMOD FMRI BUSCAD NO ELS GUARDEM
				k=k+1
		print(k)
	
			




	
	


print(temps_de_conversio('Resting State fMRI')) 



































	


			
