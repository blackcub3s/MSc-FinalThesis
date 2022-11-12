# -*- coding: utf-8 -*-
"""
Created on Fri Mar  2 15:34:27 2018

NOTA: ES PODEN CANVIAR ELS SUBJECTES DE POSICIÓ DINS DE CADA GRUP. PERO SOTA CAP CONCEPTE
ES PODEN CANVIAR DE LLOC ELS GRUPS. EN CAS CONTRARI L'ANALISIS DE SUBGRUPS ES DESTAROTARIA!!!

INDEXOS ESTARAN A ll_ids SEMPRE -->VARIABLE GLOAL
@author: santi
"""



import scipy.io as sio
import pandas as pd
import time
import seaborn as sns
import matplotlib.pyplot as plt
import os
import numpy as np

# NOTA: SI VOLEU GENERAR DE NOU ELS GRAFICS ROIxROI (un per subjecte), poseu TRUE en cridar la funcio
# crea_matrius_correlacions_ROIxROI_I_matriu_SUBJECTxSUBJECT(Genera_i_guarda_grafics_ROIxROI=False)



#carrego dades amb els IDs i mes variables:
# ESTRUCTURA df_subjecteS:
	#subject index,diagnosis,age,study years,education,gender,APOE,AB-42,t-tau,p-tau,CBF index,handedness,AL,AT,RDL,RDT
df_subjectes = pd.read_csv("subject_info.csv")


#carrego les dades de l'automatic anatomic labeling com a varible global
with open("./docs/aal_labels_LR.txt","r") as fitxer_AAL:
	llista_AAL = []
	for linia in fitxer_AAL:
		linia = linia[:-1] #trec salt de linia
		linia = ' '.join(linia.split('_')) #trec barres baixes i les substitueixo per espais en blanc
		llista_AAL = llista_AAL + [linia]



# carrego dades del fitxer de variables de matlab que conté 
# les time series... dic_time_series (ho carrega com un dic).
# De les variables que té (els noms de les quals queden aquí registrats com a claus
# i els seus nombres com a valors del diccionari) només n'hi ha 3 que contenenn info:
#     -'file_names'
#     -'TS'
#     -'subject_ID',
# 
#A la funcio pren_ids_del_csv veiem que, com era d'esperar, coincidien amb les de la variable
# "subject index" del CSV, que obtenim a la funció pren_ids_del_csv:

#dic_time series té Fitxer ['__header__', '__version__', '__globals__', 
#'file_names', 'TS', 'subject_id']  lo únic important és, basicament TS i pots pillar
# els ids de subject_id  o de file_names o de ll_ids del csv (v funcio pren ids del csv)
dic_time_series = sio.loadmat("alzheimers_3rd_TS.mat") #

#carrego les series temporals
arr_TS = dic_time_series["TS"]  #fent arr_TS.shape --> (90,290,109) --> (ROI,Time series,Subjectes)


""" ESBORRA AQUESTOS SUBJECTES PROBLEMATICS DE L'ANALISIS. TENEN
PROBLEMA A LES TIME SERIES DE LA ROI 74: TENEN NANs a la ROI Parietal SUP R """

SUBJECTES_PROBLEMATICS = ['c116','c187','c335','c389','c395','g126','g146','g240','g251','g272','g428','k324','k348','k432','p203']
INDEXS_SUBJECTES_PROBLEMA = [2, 6, 14, 16, 18, 60, 62, 68, 69, 72, 79, 90, 92, 93, 100]







def pren_ids_del_csv():
	"""poso en una llista (ll_ids) PROVINENTS de subject_info.csv
	 ordenació per defecte (i significat):
	#  1) comença per c --> Control
	#  2) comença per g --> MCI
	#  3) comença per k --> alzheimer
	#  4) comença per p --> preclinic"""
	ll_ids = []
	for id in df_subjectes["subject index"]:
		ll_ids = ll_ids + [id]
	return ll_ids

 #carrego els els 109 codis del subjecte ['c101','c114','c116', ... ,'p514','p539'] a ll_ids com a variable global
ll_ids = pren_ids_del_csv() 

#ESBORRO SUBJECTES PROBLEMA de ll_ids (ll_ids passarà a tenir 94 subjectes en comptes de 109)
for subjecte_problema in SUBJECTES_PROBLEMATICS:
	del(ll_ids[ll_ids.index(subjecte_problema)]) #ojo amb els indexos variables! :)

#ESBORRO SUBJECTES PROBLEMA de l'arr_TS: abans tenia shape (90,290,109) 
# 109 son els subjectes i estan a la tercera dimensio, columnes (o sigui index 2)
arr_TS = np.delete(arr_TS, INDEXS_SUBJECTES_PROBLEMA, axis = 2) #
#print(arr_TS.shape) #--> ara es, en efecte (90,290,94). De 109 a 94 perque treus 15 subjectes.





#FAIG DOS FUNCIONS PER A FER ELS TÍTOLS DE CADA GRÀFIC ROIxROI per a cada subjecte
#########################################################################
def categoritza_enfermetat(id): 
	"""
	treu diagnostic a partir de l'ID del subjecte (sense mirar
	el camp del diagnostic, que és redundant).
	
	#  1) comença per c --> Control
	#  2) comença per g --> MCI
	#  3) comença per k --> alzheimer
	#  4) comença per p --> preclinic
	"""
	lli = id[0] #pillo lletra que identifica enfermetat
	id = "Subject "+id #afegeixo nom
	if lli == 'c':
		diagnostic = 'Control'
	elif lli == 'g':
		diagnostic = 'MCI'
	elif lli == 'k':
		diagnostic = 'Alzheimer' 
	else: #p --> preclinic
		diagnostic = 'Preclinical'
	return diagnostic

def fes_titol_grafic_ROIxROI(id):
	diagnostic = categoritza_enfermetat(id)
	titol = 'Subjecte '+ id + ' ' + '(' + diagnostic + ')'
	return titol 

def fes_label_SUBJECTxSUBJECT(id):
	diagnostic = categoritza_enfermetat(id)
	titol = id + ' ' + '(' + diagnostic + ')'
	return titol 
	
##############################



class Grafics:
	"""
	Classe que pren una matriu 2D i la ploteja. Va bé per a gràfics ROIxROI i per a SUBJECTExSUBJECTE
	"""
	def __init__(self,matriudades):
		self.d = matriudades
	def grafic_correlacions_seaborn(self,titol):
		"""
		CODI ADAPTAT DE https://seaborn.pydata.org/examples/many_pairwise_correlations.html
		Serveix per fer un grafic de una matriu de correlacions.

		ARGUMENT_ INDEX_TITOL: el títol del gràfic.
		"""
		sns.set(style="white")

		# Compute the correlation matrix
		corr = self.d  #aqui self.d conté la matriu de correlacions perquè cridem aquesta funció des de metode matriu_correlacions.	

		# Generate a mask for the upper triangle
		mask = np.zeros_like(corr, dtype=np.bool)
		mask[np.triu_indices_from(mask)] = False

		# Set up the matplotlib figure
		f, ax = plt.subplots(figsize=(11, 9))
		

		# Generate a custom diverging colormap
		cmap = sns.diverging_palette(220, 10, as_cmap=True)

		# Draw the heatmap with the mask and correct aspect ratio
		sns.heatmap(corr, mask=mask, cmap=cmap, vmax=1, center=0,
		            square=True, linewidths=.0, cbar_kws={"shrink": .5})		

		plt.title(titol)




def elimina_tri_superior_i_flateneja_ROIxROI(m_correl):
	"""
	Aquest mètode pren un pandas dataframe (m_correl) que conté una matriu de correlacions
	nxn (ROIxROI), n'elimina el triangle superior i la diagnoal principal i en retorna
	el que hi ha a returns.
	
	RETURNS: Un objecte tipus list. concretament un
	vector (fila) de (1/2)*n(n-1) correlacions (elements). Si ROIxROI d'entrada
	es 90x90, el vector que es retorna tindrà 4005 valors.
	
	RETURNS: objecte tipus list d'una sola dimensio
	es 90x90.
	
	NOTA:
		
	Podria ser temptador fer servir la funció numpy.tril, però no ens flateneja l'array
	ni tampoc ens treu els elements que ocupen el triangle
	superior ni la diagonal principal (per tant, igualment ho hauriem de fer nosaltres
	manualment...
	"""
	

	#m_correl es dataframe de pandas. com que vull operar com a llista...
	# FAIG A LA SEGUENT LINIA LE PAS dataframe ----> array numpy ----> llista
	ll_correl = m_correl.values #dataframe -->ndarray 
	ll_correl = ll_correl.tolist() #ndarray --> llista
	#time.sleep(10)
	ll_ROIxROI_flattened = []
	for i in range(1,len(ll_correl)):
		bufer = ll_correl[i][:i]
		ll_ROIxROI_flattened = ll_ROIxROI_flattened + bufer
	return ll_ROIxROI_flattened


def mitjana_stack_element_wise(m): #m es un stack de ROIxROIs, perteneixent a una mateixa categoria!
	"""
	ARGUMENT ENTRADA: tensor -numpy ndarray- de shape (l,m,n) --> MATRIU ROIxROI per exemple!!
	RETURN: matriu -numpy ndarray- de shape (m,n).
	
	EXPLICACIÓ: Donat un tensor 3D d'entrada de shape (l,m,n) aquesta funció ens 
	computa la mitjana aritmètica per cada posició ij de totes les l submatrius 
	de shape (m,n).
	
	ÚS: Es fa servir per tal de, donada una categoria de pacients, mirar les correlacions
	mitjanes dins de cada ROI, i plotejar-les en una matriu ROIxROI de shape (m,n) que resumeixi
	les correlacions mitjanes intragrup en una sola matriu.
	
	veure document EXPLICACIÓ 3
	
	"""
	arr_ROIxROI_correlacions_mitjanes = np.zeros((m[0].shape))
	nre_matrius_stack = len(m)
	for i in range(len(m[0])): #recorro files de cada submatriu de shape (m,n). len(m[0]) es m files
		for j in range(len(m[0][0])): #recorro columnes de cada submatriu de shape (m,n). len(m[0][0]) son les n columnes.
			arr_correlacions_ROI = m[:,i,j]
			arr_ROIxROI_correlacions_mitjanes[i][j] = sum(arr_correlacions_ROI)/nre_matrius_stack #mitjana aritmètica de de les correlacions dins de cada ROI
	return arr_ROIxROI_correlacions_mitjanes



def comprova_nan(index_ROI):
	#FUNCIO QUE COMPROVA UNA SOLA ROI DONADA DE arr_TS.
	ROI = arr_TS[index_ROI].transpose()   #despres de transposar tinc 109,290 [subjectes a files, TS a columnes]
	Subjectes_problema_ROI = []
	for i in range(len(ROI)):
		for j in range(len(ROI[0])):
			if np.isnan(ROI[i][j]):
				Subjectes_problema_ROI += [i] 
				break
	return Subjectes_problema_ROI

#print(comprova_nan(74)) 


def comprova_tot():
	ll = []		
	for i in range(len(arr_TS)):  #recorro totes les ROIs i comprovo si hi ha subjectes problematics. Que en eprincipi no!
		roi = comprova_nan(i)
		if len(roi)>0: #SI ESTA BUIT, NO HI HA CAP PROBLEMA PER A CAP SUBJECTE A LA ROI i DONADA
			ll = ll + [i,roi] # PROBLEMA A ROI 74.
	
	for subjecte_problema in ll[1]:
		pavos_problematics_ROI74 = [] #teenen un o diversos o tots NAN
		pavos_problematics_ROI74 +=  [ll_ids[subjecte_problema]]
		print(pavos_problematics_ROI74)

#comprova_tot()


class tracta_time_series:
	def __init__(self): 
		""" Mètode init carrega la variable global arr_TS que ve del fitxer de matlab"""
		self.M = arr_TS  # Arr_TS recorda que té -quan no esborres subjecte problematic- (90,290,109)   --> (ROIs, Time Series, Subjectes)
		
																#   [stack_matrius, files, columnes]
		
	def transposa_tensor(self):
		"""
		Mètode que transposa arr_TS (ara self.M). Per entendre de quin tensor partim
		i a quin tensor ho convertim després de la transposició veure la imatge "s__fitxer transposicio.jpg"
		
		
		Després de la transposicio la shape de la matriu 3D és (109,290,90). Així tinc 
		un stack de 109 matrius (una per cada subjecte), on es tenen les 290 series temporals disposades
		en files, i les 90 ROIs  de l'AAL (Automatic Anatomic Labeling) a les columnes. 
		
		La representació gràficad'aquest pas (de arr_TS a la seva
		transposada està al fitxer transposicio.jpg)
		
		Es important que les rois estiguin a columnes perquè puguem tractar-les
		com a variables per fer les matrius de correlacions ROI x ROI.
		
		La matriu transposada servirà per fer les matrius de correlacions directament.
		Alternativament haguessim pogut no transposar la matriu 3D de cop. 
		Sino recorrer cada slice de numpy i transposarlo (**1) i, acte seguit,
		fer cada matriu 2D segons:  
		
			for i in range(len(self.M[0][0])): #ojo aqui amb les dimensions!
				matriu_2d = self.M[:,:,i].transpose() 
				#fer matriu correlacions per cada matriu_2d (subjecte)
		
		Els dos mètodes són igual d'eficients computacionalment però és més senzill el primer. 
		Com a curiositat, a l'arxiu "comparació eficiències" es pot veure quin dels dos
		mètodes és més ràpid. Els dos són igual de ràpids. 

		"""
		return self.M.transpose() #ara la matriu té (109,290,90) --> (Subjectes, Time Series, ROIs)
																					#[stack_matrius, files, columnes]

	def crea_matrius_correlacions_ROIxROI_I_matriu_SUBJECTxSUBJECT(self, Genera_i_guarda_grafics_ROIxROI, genera_arrays_per_a_analisi_de_subgrups):
		"""
		Genero matrius de correlacions ROIxROI per cada subjecte. Faig gràfics de cada
		una incloient nom del subjecte (id) i patologia (tant al títol del gràfic com al del
		png generat), i les AALs incluides al gràfic. 
		
		Inputs: Si Genera_i_guarda_grafics_ROIxROI és false, no els generarà (perquè tarda molt
		i ja els he fet)
		
		Outputs: retorna una array de numpy de shape [109,90,90] (basicament trec un stack
		de matrius ROIxROI -o sigui shape 90x90-). la matriu [N,n,n] 
		"""
		#importo la matriu transposada de la funcio naterior
		tensor_pacients = tracta_time_series.transposa_tensor(self)#ara la matriu té (109,290,90) --> (Subjectes, Time Series, ROIs)
																					#[stack_matrius, files, columnes]

		directori_guardar_ROIxROI = 'matrius_ROIxROI_DESPRÉS_15_SUBJECTES_ELIMINATS'
		#crea una carpeta per guardar les matrius ROIxROI que generaràs ara:
		if not os.path.exists("./"+directori_guardar_ROIxROI):
			os.makedirs("./"+directori_guardar_ROIxROI)
		else:
			pass

		# RECORRO CADA MATRIU (UNA PER SUBJECTE) DINS EL TENSOR_PACIENTS. 
		# FAIG MATRIU I GRÀFIC DE CORRELACIONS.
		# OBTINC MATRIU ([ROIxROI,PACIENTS], QUE ANIRÀ DINS ll_ROI_flattened)
		ll_ROIxROI_flattened = []
		
		#GENERO LES LLISTES BUIDES PER POSAR LES ROIxROI per cada categoria
		if genera_arrays_per_a_analisi_de_subgrups:
			arr_ROIxROIs_controls = []
			arr_ROIxROIs_MCIs = []
			arr_ROIxROIs_alzh = []
			arr_ROIxROIs_preclin = []			
		
		for i in range(len(tensor_pacients)): #matriu_subjecte --> (290,90) --> 90 ROI (90 COLS), 290 series temp (290 FILES)  
			matriu_subjecte = tensor_pacients[i]
			matriu_subjecte = pd.DataFrame(data = matriu_subjecte, columns = llista_AAL) #passo a dataframe i poso labels AAL per a les ROI
			ROIxROI = matriu_subjecte.corr() #faig matriu de correlacions ROIxROI per al subjecte donat  (shape ROIxROI --> [90,90]) 
			id_subjecte = ll_ids[i] #carrego com a titol del grafic el nom del pacient
			#GUARDO LES MATRIUS ROIxROI en un stack
			
			if Genera_i_guarda_grafics_ROIxROI:
				titol_grafic = fes_titol_grafic_ROIxROI(id_subjecte) #crido la funcio que fa el titol
				Grafics(ROIxROI).grafic_correlacions_seaborn(titol_grafic) #faig el gràfic amb seaborn
				plt.savefig('./'+directori_guardar_ROIxROI+'/'+titol_grafic+".png")	#guardo els grafics
				#plt.show()

			# ANALISI EXTRA: GUARDO LES matrius ROIxROI per grups per a cridar després
			# en la funció crea_una_sola_ROIxROI_per_cada_subgrup per analitzar-ho tot
			if genera_arrays_per_a_analisi_de_subgrups:
				#CREO LES ARRAYS per guardar les matrius ROIxROI per als subjectes de 
				# cada subgrup/patologia/categoria, dis-li com vulguis
				
				#PASSO variable ROIxROI, que es pandas dataframe, a numpy array
				arr_ROIxROI = ROIxROI.values
				
				#TROCEJO LA MOSTRA EN CADA CATEGORIA. CREO TENSORS 3D.
				#ojo arr encara no son arrays. Son llistess!!!!
				


				if id_subjecte[0] == 'c': #C SON CONTROLS
					arr_ROIxROIs_controls = arr_ROIxROIs_controls + [arr_ROIxROI]
				elif id_subjecte[0] =='g': #g SON MCI
					arr_ROIxROIs_MCIs = arr_ROIxROIs_MCIs + [arr_ROIxROI]					
				elif id_subjecte[0] == 'k': #K SON ALZHEIMERS
					arr_ROIxROIs_alzh = arr_ROIxROIs_alzh + [arr_ROIxROI]
				else: #P SON PRECLINICS
					arr_ROIxROIs_preclin = arr_ROIxROIs_preclin + [arr_ROIxROI]					
				
				
			#ARA FAIG ELS PASSOS ETIQUETATS COM A STEP3 + STEP 4 AL fitxer s__ANALISIS:
			#elimino diag principal + tri sup i flatenejo (mantinc mateix nom de la variable per eficiencia):
			ROIxROI_flattened = elimina_tri_superior_i_flateneja_ROIxROI(ROIxROI) #ROIxROI_flattened té, després d'aquesta linia forma lista de long [4005] (JA QUE ROIs = 90)
			ll_ROIxROI_flattened = ll_ROIxROI_flattened + [ROIxROI_flattened]
		arr_ROIxROI_flattened = np.array(ll_ROIxROI_flattened) #arr_ROIxROI_flattened es de shape (109,4005). Es a dir, 109 pacients (109 files) i 4005 correlacions entre ROI per cada un (4005 columnes)
		arr_ROIxROI_flattened = arr_ROIxROI_flattened.transpose()
		
		
		if genera_arrays_per_a_analisi_de_subgrups:
			# arr_X en realitat, fins ara, son llistes amb arrays com a elements
			# volem que tot sigui array per a fer les mitjanes a través de la primera
			# dimensió (dimensio de l'stack). A convertir doncs!    #(SUBJECTES_PER_CATEGORIA,ROI,ROI)

			arr_ROIxROIs_controls = np.array(arr_ROIxROIs_controls) #   (58,90,90)
			arr_ROIxROIs_MCIs = np.array(arr_ROIxROIs_MCIs)         #   (23,90,90)
			arr_ROIxROIs_alzh = np.array(arr_ROIxROIs_alzh)	        #   (16,90,90)
			arr_ROIxROIs_preclin = np.array(arr_ROIxROIs_preclin)   #   (12,90,90) 
	
			
			#I ARA ANALITZO CADA SUBGRUP OBTENINT UNA SOLA ROIxROI per cada un.
			# CADA ROIi x ROIj és la mitjana al llarg de la dimensió de l'stack de matrius
			# per a aquella posició ij donada. Podeu veure, de nou, fitxer EXPLICACIO_3.jpg
			
			#SON NDARRAYS, DE MOMENT!!!
			ROIxROI_correlacions_mitjanes_controls = pd.DataFrame(data = mitjana_stack_element_wise(arr_ROIxROIs_controls),columns=llista_AAL)
			ROIxROI_correlacions_mitjanes_MCIs = pd.DataFrame(data = mitjana_stack_element_wise(arr_ROIxROIs_MCIs), columns = llista_AAL)
			ROIxROI_correlacions_mitjanes_alzh = pd.DataFrame(data = mitjana_stack_element_wise(arr_ROIxROIs_alzh), columns = llista_AAL)
			ROIxROI_correlacions_mitjanes_preclin = pd.DataFrame(data = mitjana_stack_element_wise(arr_ROIxROIs_preclin), columns = llista_AAL)

			#OBTINC MATRIUS DE CORRELACIONS
			
			#ROIxROI_correlacions_mitjanes_MCIs
			#ROIxROI_correlacions_mitjanes_alzh
			#ROIxROI_correlacions_mitjanes_preclin

			#PLOTEJO MATRIUS I HI POSO TITOLS
			titol_grafic = "ROI x ROI | mitjana de totes les cel·les ROIxROI individuals en "
			
			
			Grafics(ROIxROI_correlacions_mitjanes_controls).grafic_correlacions_seaborn(titol_grafic+" CONTROLS")
			plt.savefig(titol_grafic+" CONTROLS.png")	#guardo grafic NO FUNCIONA BÉ
			Grafics(ROIxROI_correlacions_mitjanes_MCIs).grafic_correlacions_seaborn(titol_grafic+" MCIs")
			#plt.savefig(titol_grafic+" MCIs.png")	#guardo grafic NO FUNCIONA BÉ
			Grafics(ROIxROI_correlacions_mitjanes_alzh).grafic_correlacions_seaborn(titol_grafic+" ALZHEIMER")
			#plt.savefig(titol_grafic+" Alzh.png")	#guardo grafic NO FUNCIONA BÉ
			Grafics(ROIxROI_correlacions_mitjanes_preclin).grafic_correlacions_seaborn(titol_grafic+" PRECLÍNICS")
			#plt.savefig(titol_grafic+" Preclin.png")	#guardo grafic NO FUNCIONA BÉ
	

				#plt.show()







		#OBTINC I RETORNO LA MATRIU ja transposada. 
		return arr_ROIxROI_flattened #shape (4005,109) --> pacients a columnes. Llest per a fer la matriu de correlacions... de correlacions (bis). Shape---> SUBJECTxSUBJECT
		
	def fes_grafic_SUBJECTxSUBJECT(self, mostra_grafic):
		#AGAFO LA MATRIU SUBJECTxSUBJECT que retorna la funció anterior (alla en deia arr_ROIxROI_flattened)
		arr_ROIxROI_flattened = tracta_time_series().crea_matrius_correlacions_ROIxROI_I_matriu_SUBJECTxSUBJECT(Genera_i_guarda_grafics_ROIxROI=False, genera_arrays_per_a_analisi_de_subgrups=False)
		
		#FAIG LES ETIQUETES PER A CADA COLUMNA
		ll_ids_subjectes = pren_ids_del_csv()
		ll_etiq = []
		for id in ll_ids_subjectes:
			etiqueta = fes_label_SUBJECTxSUBJECT(id)
			ll_etiq = ll_etiq + [etiqueta]
		
		# CONVERTEIXO arr_ROIxROI_flattened a DATAFRAME DE PANDAS I AFEGEIXO 
		# LES ETIQUETES (noms dels subjectes amb l'enfermetat) A LES COLUMNES
		df_ROIxROI_flattened = pd.DataFrame(data = arr_ROIxROI_flattened, columns = ll_etiq)
		
		#FAIG LA MATRIU DE CORRELACIONS SUBJECTxSUBJECT 
		df_SUBJECTxSUBJECT = df_ROIxROI_flattened.corr() #(surt 109x109 --> (109 subj))
		
		#FAIG EL GRÀFIC DE LA MATRIU DE CORRELACIONS SUBJECTxSUBJECT, AFEGINT ETIQUETES I DIAGNOSTICS
		titol_grafic = "matriu correlacions SUBJECTxSUBJECT"
		Grafics(df_SUBJECTxSUBJECT).grafic_correlacions_seaborn(titol_grafic)
		
		#MOSTRO GRAFIC (SI ES EL CAS)
		if mostra_grafic:
			plt.show()
			
		#CREO DIRECTORI PER GUARDAR LA FIGURA
		directori_guardar_SUBJECTxSUBJECT = "matriu_SUBJECTxSUBJECT"
		if not os.path.exists("./"+directori_guardar_SUBJECTxSUBJECT):
			os.makedirs("./"+directori_guardar_SUBJECTxSUBJECT)
		else:
			pass
		
		#GUARDO EL GRÀFIC [NO EL GUARDA B]
		#plt.savefig('./'+directori_guardar_SUBJECTxSUBJECT+'/'+titol_grafic+".png") #NO SE PER QUE NO EL GUARDA B
		
		#EN ACABAR DESCOMENTA 480 i 477
	def grafic_entre_dues_rois_per_a_un_subjecte_donat(self, estandaritza_TS):
		"""Computo el gràfic entre dues ROIsDONADES.
		"""
		import matplotlib.pyplot as plt
		from scipy.stats import pearsonr
		
		#PARÀMETRES DEL GRÀFIC (ELS POTS CANVIAR PER MOURE'T PEL TENSOR DE SERIES TEMPORALS)
		subjecte_index = 0 #index del subjecte (0 a 94 o 109 -depenent de si elimino subjectes amb NANs o no, respectivament-)
		ROI1_index = 0 #PRECENTRAL L
		ROI2_index = 2 #FRONTAL SUB ORB L
		
		#CARREGO_DADES
		tensor_pacients = tracta_time_series.transposa_tensor(self)
		M = tensor_pacients[subjecte_index] #X te un pacient sa (pacient 0, shape 290,90)
		
		if estandaritza_TS:
			dt_ROI1, dt_ROI2 = np.std(M[:,ROI1_index]), np.std(M[:,ROI2_index])
			x_ROI1, x_ROI2 = np.mean(M[:,ROI1_index]), np.mean(M[:,ROI2_index])
			
			TS_ROI1 = ((M[:,ROI1_index] - x_ROI1)/dt_ROI1)#+2
			TS_ROI2 = ((M[:,ROI2_index] - x_ROI2)/dt_ROI2)#-2
			
			print(np.mean(TS_ROI1), np.std(TS_ROI1))
		else:
			TS_ROI1 = M[:,ROI1_index]
			TS_ROI2 = M[:,ROI2_index]		
		
		#GRAFIC de les dues TIME SERIES (BOLD --> BOLD)
		plt.plot(TS_ROI1,TS_ROI2,"or")
		if estandaritza_TS:
			plt.xlabel(llista_AAL[ROI1_index]+" (BOLD, z-score)")
			plt.ylabel(llista_AAL[ROI2_index]+" (BOLD, z-score)")
		else:
			plt.xlabel(llista_AAL[ROI1_index]+" (BOLD, z-score)")
			plt.ylabel(llista_AAL[ROI2_index]+" (BOLD, z-score)")
		plt.title("Subject "+ll_ids[subjecte_index])
		plt.show()
		print("r = {:.2f} p = {:.4f}".format(pearsonr(TS_ROI1,TS_ROI2)[0],pearsonr(TS_ROI1, TS_ROI2)[1]))
		
		X = np.arange(1,290+1,1)
		#2 SUBGRAFICS (UN PER ROI) EIXOS --> TIME SERIES --> BOLD
		plt.plot(X,TS_ROI1,"ro" , label = llista_AAL[ROI1_index])
		plt.plot(X,TS_ROI2,"go", label = llista_AAL[ROI2_index])

		plt.xlabel ("Time Series")
		if estandaritza_TS:
			plt.ylabel ("BOLD, z-score")
		else:
			plt.ylabel ("BOLD")
		
		plt.legend()
		
		plt.title("Subject "+ll_ids[subjecte_index])
		plt.show()
			
#GRAFICS
#tracta_time_series().grafic_entre_dues_rois_per_a_un_subjecte_donat(estandaritza_TS = True)
			
#MATRIUS ROIxROI (fMRI, functional connectivity)		
#tracta_time_series().crea_matrius_correlacions_ROIxROI_I_matriu_SUBJECTxSUBJECT(Genera_i_guarda_grafics_ROIxROI=False, genera_arrays_per_a_analisi_de_subgrups=True)

#MATRIU SUBJECTxSUBJECT (correlacions entre els subjectes: variablecorrelacionada entre subjectes: "correlacions entre les ROIs" ).
#tracta_time_series().fes_grafic_SUBJECTxSUBJECT(mostra_grafic=False)




#############################################################
#		aqui a sota van els analisis de DTI. Poden cridar funcions definides abans
###############################################################			



		
			
		
		
		
		
		
		
		
		
		
		
		
		


































		
		
		
		
		
		
		
def compara_ordre_ids():
	"""
	He fet aquesta funció per comprovar que quadra l'ordre dels subjectes (i que hi ha els mateixos)
	subjectes a les diferents estructures on han d'estar-hi: dins el fitxer csv "subject_info.csv" (columna), a la 
	columna subject index (guardat aqui com a ll_ids), i a les dues variables del fitxer de matlab .mat, 
	variables file_names i subject_id. Després de fer la funció veiem que tot quadra.
	"""
	#imprimeixo les claus del diccionari:
	print("noms de les claus (variables) registrades a time series")
	print(list(dic_time_series)) 
	#__header__, __version__ i __globals__ no contenen res útil. Cal mirar
	# els valors que el dic_time_series té dins a les 
	# tres claus seguents: 'file_names', 'TS', 'subject_id'
	
	#FILE_NAMES conté els noms organitzats en el mateix ordre de ll_ids
	arr_file_names = dic_time_series["file_names"]   #  té 109 subjectes       ######
	arr_TS = dic_time_series["TS"]                   #  té 90, un per cada ROI ######
	arr_subject_id = dic_time_series['subject_id'][0]#  té 109 subjectes       #######
	
	
	# COMPROVO QUE, EN EFECTE, L'ORDE DELS IDs definits A arr_file_names
	# (del fitxer de matlab) coincideix amb el definit a 
	# ll_ids (prvinent del fitxer csv) i alhora amb el de arr_subject_id()
	#import time
	
	ll_ids = pren_ids_del_csv()
	error = False
	for i in range(len(arr_file_names)):
		if 	arr_file_names[i][0][0][6:10] == ll_ids[i] == arr_subject_id[i][0]:
			#print(arr_file_names[i][0][0][6:10],ll_ids[i],arr_subject_id[i][0])
			#time.sleep(1)
			pass
		else:
			raise ValueError("Algun o diversos dels ids introduits\n No coincideixen en ordre o forma")
			error = True
	if not error:
		print("ordre dels subjectes a través de les variables, quadra :) :)")
	print("(ROI,Tseries,Subjectes) --> "+str(arr_TS.shape))
	
	print(len(arr_TS[0][0]))


#analitza_dic_time_series()	
		
		
		
		