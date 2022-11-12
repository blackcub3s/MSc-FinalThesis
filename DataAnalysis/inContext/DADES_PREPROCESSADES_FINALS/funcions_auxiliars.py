# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 23:12:42 2018

@author: santi
"""
import numpy as np
from sklearn.metrics import confusion_matrix
import time
def comprova_nans(M_3D):
	"""
	Funcio que donada una matriu 3D cerca els NANs i torna els indexos
	de la PRIMERA dimensio on hi ha problemes, en forma de llista (k,i,j)
	"""

	ll = []
	for k in range(len(M_3D)): #RECORRO STACK
		for i in range(len(M_3D[0])): #RECORRO FILA
			for j in range(len(M_3D[0][0])): #RECORRO COLUMNA
				if np.isnan(M_3D[k][i][j]):
					ll = ll + [(k,i,j)]
	if ll == []:
		print("No hi ha errors per NaN... la matriu 3D esta neta")
	else:
		print("Hi ha els seguents errors per NaN a la matriu 3D (k,i,j) --> (stack, fila,col:")
		print(ll_errors_na)
					
					
def elimina_tri_superior_i_flateneja_ROIxROI(m_correl):
	"""
	Aquest mètode pren una array de numpy que conté una matriu de correlacionsnxn anomenada m_correl (ROIxROI), n'elimina el triangle superior i la diagonal principal i en retornael que hi ha a returns.
	
	RETURNS: Un objecte tipus list. concretament unvector (fila) de (1/2)*n(n-1) correlacions (elements). Si ROIxROI d'entrada
	es 90x90, el vector que es retorna tindrà 4005 valors. Si es 214x214 -shen- obtindrà22 791 valors...

	NOTA:		
	Podria ser temptador fer servir la funció numpy.tril, però no ens flateneja l'arrayni tampoc ens treu els elements que ocupen el triangle
	superior ni la diagonal principal (per tant, igualment ho hauriem de fer nosaltresmanualment...
	"""
	#m_correl es dataframe de pandas. com que vull operar com a llista... || FAIG A LA SEGUENT LINIA LE PAS dataframe ----> array numpy ----> llista
	ll_correl = m_correl.tolist() #ndarray --> llista 
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




def evalua_normalitat_i_homocedasticitat_DISTRIBUCIONSFMRI(variable_MCIc, variable_MCInc, centre):
	from scipy import stats
	shapiro_MCIc, p_shapiro_MCIc = stats.shapiro(variable_MCIc);  shapiro_MCInc, p_shapiro_MCInc = stats.shapiro(variable_MCInc)
	levene_statistic, p_levene = stats.levene(variable_MCIc, variable_MCInc)
	t_test = False
	if p_shapiro_MCIc < 0.05 or p_shapiro_MCInc < 0.05: #Si la variable NO ES NORMAL segons shapiro wilk
		if p_levene < 0.05: #si no hi ha homogeneitat de variances
			print('{:7}   {:.2f} (p = {:.5f}) | {:.2f} (p = {:.5f})* ||| {:.2f} (p = {:.3f})+[mw]'.format(str(centre),shapiro_MCIc, p_shapiro_MCIc, shapiro_MCInc, p_shapiro_MCInc, levene_statistic, p_levene))
		else:#si hi ha homogeneitat de variances
			print('{:7}   {:.2f} (p = {:.5f}) | {:.2f} (p = {:.5f})* ||| {:.2f} (p = {:.3f})[mw]'.format(str(centre),shapiro_MCIc, p_shapiro_MCIc, shapiro_MCInc, p_shapiro_MCInc, levene_statistic, p_levene))
	else:#si la variable es normal segons shapiro wilk
		if p_levene < 0.05:#si no hi ha homogeneitat de variances
			print('{:7}   {:.2f} (p = {:.5f}) | {:.2f} (p = {:.5f}) ||| {:.2f} (p = {:.3f})+[mw]'.format(str(centre),shapiro_MCIc, p_shapiro_MCIc, shapiro_MCInc, p_shapiro_MCInc, levene_statistic, p_levene))
		else: #si hi ha homogeneitat de variances
			print('{:7}   {:.2f} (p = {:.5f}) | {:.2f} (p = {:.5f})  ||| {:.2f} (p = {:.3f}) [t]'.format(str(centre),shapiro_MCIc, p_shapiro_MCIc, shapiro_MCInc, p_shapiro_MCInc, levene_statistic, p_levene))
			t_test = True
	return t_test











def bivariant_comparacio_mitjanes(X,Y,t_test):
	from scipy.stats import ttest_ind, mannwhitneyu
	"""
	INPUTS: Dies Lliste de python (list) amb les Variables quantitatives en tipus integer/float. t_test es un boolea que diu si aplicar t-test (true) o mannwhitney (false)  
	FUNCIÓ: Aplica un contrast d'hipòtesis per comparar les mitjanes de les dues variables X i Y. 
			Si hi ha homocedasticitat aplica un t-test (la funció evalua prova levene); en cas contrari aplica un mann-whitney. Els NaN 
			els omet tots.
	RETURNS: floats amb el test, el p valor. Un boolea anomenat "t_Test" amb True si la funcio retorna un t-test i false si torna un mann whitney
	"""
	if t_test: #si hi ha homocedasticitat i hi ha normalitat aplico la prova paramètrica (t-test)
		t_test, p_valor = ttest_ind(X,Y)[0],ttest_ind(X,Y)[1]  #,nan_policy='omit'  HO TREC PERQUE JA ELS HE ELIMINAT A b. analisis final
		return t_test, p_valor, t_test
	else: #si no hi ha normalitat, o hi és però no hi ha homocedasticitat i no puc aplicar el t test aplico mann-whitney
		mw_test, p_valor = mannwhitneyu(X,Y)[0], mannwhitneyu(X,Y)[1]
		return mw_test, p_valor, t_test
		#return mann-whit, p-valor


def imprimeix_i_retorna_mesures_dexactitud_diagnostica(ll_labels,ll_predits):
	"""
	inputs: ll_labels es una llista amb la ground truth, les etiquetes, o el gold standard. ll_predits és una llista amb els valors predits 
	pel model. Ojo, "ll_predits" es valo enter. No posem aqui els logits, sino el redondeig dels logits l'enter mes proper.
	"""
	tn, fp, fn, tp = confusion_matrix(ll_labels, ll_predits).ravel()
	s, e = tp/(tp+fn), tn/(fp+tn)
	print("\n#######################")
	print("Accuracy: {:.5f}".format((tp+tn)/(tp+tn+fp+fn)))
	print("Sensibilitat: {:.5f}".format(s))
	print("Especificitat: {:.5f}".format(e))
	print("Valor predictiu + (PPV): {:.5f}".format(tp/(tp+fp))) #tambe anomenat precision score. hi ha una funcio a sklearn que ho fa
	print("Valor predictiu - (NPV): {:.5f}".format(tn/(fn+tn)))
	print("LR+: {:.5f}".format(s / (1 - e)))
	print("LR-: {:.5f}".format((1 - s)/e))
	print("#######################")
	print("tn,fp,fn,tp: ",tn,fp,fn,tp)
	print("#######################\n")
	return tn, fp, fn, tp





def plot_pdf_FC_centres(FC_vectoritzada,ll_codis_centre,df):
	import matplotlib.pyplot as plt
	import seaborn as sns
	from scipy.stats import ttest_ind, mannwhitneyu
	"""	
	AIXO VA EN TANDEM A LA TAULA DE ANNEX "Number of participants by site and study group".
	PLOTEJEM ELS TRES CENTRES MES FREQUENTS. TENEN CODIS SITE = 1, 53 i 22. Corresponen a 001, 130 i 006 de la variable PTID amb ids de subjectes, respectivament.
	"""
	#print(FC_vectoritzada.shape," --> (74,22k)")
	sns.set(color_codes=True) #perque surti la graella

	#####
	BW_INDIVIDUALS = .1 #AMB AQUEST PARAMETRE FAS MES O MENYS SMOOTH EL GRAFIC DE LA DISTRIBUCIO DE FCONS
	BW_GRUPALS = .1
	DPI = 300 #pixels per polzada a les figures
	####
	FC_MCIc_3centres = []
	FC_MCInc_3centres = []
	ll = [] #guardo els prints
	print("#######ASSUMPCIONS DE HOMOCEDASTICITAT I NORMALITAT#######")
	for codi_centre in ll_codis_centre:	
		ll_indexs_df = df.index[df["SITE"] == codi_centre].tolist()	

		#PAS 1) PLOTEJO PRIMER, PER A CADA CENTRE, ELS MES ABUNDANTS (ELS MCI NC... VULL QUE SURTIN DARRERE!!!)
		FC_grup_MCInc_i_centre = []
		for index_pacient in ll_indexs_df:
			FC_vectoritzada_pacient = FC_vectoritzada[index_pacient,:] #selecciono la fila de FC vectoritzada per a cada pacient
			if df["s_CONVER"].iloc[index_pacient] == 0: #PACIENT MCI-nc
				FC_grup_MCInc_i_centre += list(FC_vectoritzada_pacient)			
				sns.kdeplot(FC_vectoritzada_pacient, bw=BW_INDIVIDUALS ,shade=True, label=str(df["PTID"].iloc[index_pacient])+" (MCI-nc)")
		FC_MCInc_3centres += FC_grup_MCInc_i_centre	#GUARDO L'ACUMULAT	
		
		#PAS 2)PLOTEJO DESPRES, PER A CADA CENTRE, ELS MENYS ABUNDANTS PER CENTRE (ELS MCI-C... QUE VULL QUE SURTIN DAVANT)
		FC_grup_MCIc_i_centre = []
		for index_pacient in ll_indexs_df:
			FC_vectoritzada_pacient = FC_vectoritzada[index_pacient,:] #selecciono la fila de FC vectoritzada per a cada pacient
			if df["s_CONVER"].iloc[index_pacient] == 1: #PACIENT MCI-c
				FC_grup_MCIc_i_centre += list(FC_vectoritzada_pacient)
				sns.kdeplot(FC_vectoritzada_pacient, bw=BW_INDIVIDUALS ,shade=False, color="red", label=str(df["PTID"].iloc[index_pacient])+" (MCI-c)")
		FC_MCIc_3centres += FC_grup_MCIc_i_centre #GUARDO L'ACUMULAT
		
		#FINALMENT MOSTRO ELS PLOTS AMB DISTRIBUCIONS PER CENTRE INDIVIDUALS I LES GUARDO
		plt.title("CODE CENTER: "+str(codi_centre))
		plt.xlabel("Functional Connectivity")
		plt.ylabel("Kernel density estimates")
		plt.savefig("fig_distFC_individual_centre_"+str(codi_centre)+".png",dpi=DPI)
		#plt.show()
		plt.close()
		
		#FAIG PLOT DE DISTRIBUCIO FC PER CENTRE, GRUPALS, I LES GUARDO
		plt.title("CODE CENTER: "+str(codi_centre))
		fes_t_test = evalua_normalitat_i_homocedasticitat_DISTRIBUCIONSFMRI(FC_grup_MCIc_i_centre, FC_grup_MCInc_i_centre, "centre "+str(codi_centre))
		time.sleep(1)
		if fes_t_test:
			estadistic, p_valor = ttest_ind(FC_grup_MCIc_i_centre, FC_grup_MCInc_i_centre)[0],ttest_ind(FC_grup_MCIc_i_centre, FC_grup_MCInc_i_centre)[1]
			ll += ["MCIc vs MCInc (centre "+str(codi_centre)+") ->(ttest): "+ str(estadistic)+str(p_valor)]
		else: #fes mann whitney
			estadistic, p_valor = mannwhitneyu(FC_grup_MCIc_i_centre, FC_grup_MCInc_i_centre)[0], mannwhitneyu(FC_grup_MCIc_i_centre, FC_grup_MCInc_i_centre)[1]
			ll += ["MCIc vs MCInc (centre "+str(codi_centre)+") ->(mw): "+ str(estadistic)+str(p_valor)]
		plt.legend(str(estadistic)+","+str(p_valor))
		sns.kdeplot(FC_grup_MCInc_i_centre, bw=BW_GRUPALS ,shade=True, label="Combined FC (MCI-nc)")
		sns.kdeplot(FC_grup_MCIc_i_centre, bw=BW_GRUPALS ,shade=True, color="red", label="Combined FC (MCI-c)")
		plt.xlabel("Functional Connectivity")
		plt.savefig("fig_distFC_mitjana_centre_"+str(codi_centre)+".png",dpi=DPI)
		#plt.show()
		plt.close()			

		#DISTRIBUCIO MITJANA DELS 3 CENTRES
		plt.title("CENTRE CODES: "+str(ll_codis_centre))
		sns.kdeplot(FC_MCInc_3centres, bw=BW_GRUPALS ,shade=True, label="Combined FC (MCI-nc)")
		sns.kdeplot(FC_MCIc_3centres, bw=BW_GRUPALS ,shade=True, color="red", label="Combined FC (MCI-c)")
		plt.xlabel("Functional Connectivity")
		plt.savefig("fig_distFC_mitjana_centres_"+((str(ll_codis_centre).replace(" ","_")).replace("[","__")).replace("]","__")+".png",dpi=DPI)
		#plt.show()
		plt.close()		

	#PLOT DE TOTA LA DISTRIBUCIO (NO NOMES DELS 3 CENTRE SINO DE TOTS)
	indexos_MCIc_TOTS = list(df.index[df["s_CONVER"]==1])
	indexos_MCInc_TOTS = list(df.index[df["s_CONVER"]==0])
	FC_tots_MCIc, FC_tots_MCInc = np.hstack(FC_vectoritzada[indexos_MCIc_TOTS,:]), np.hstack(FC_vectoritzada[indexos_MCInc_TOTS,:])
	fes_t_test = evalua_normalitat_i_homocedasticitat_DISTRIBUCIONSFMRI(FC_tots_MCIc, FC_tots_MCInc, "all centers")
	if fes_t_test:
		estadistic, p_valor = ttest_ind(FC_tots_MCIc, FC_tots_MCInc)[0],ttest_ind(FC_tots_MCIc, FC_tots_MCInc)[1]
		ll += ["MCIc vs MCInc (tots els 13 centres) ->(ttest): "+str(estadistic)+","+str(p_valor)]
	else: #fes mann whitney
		estadistic, p_valor = mannwhitneyu(FC_tots_MCIc, FC_tots_MCInc)[0], mannwhitneyu(FC_tots_MCIc, FC_tots_MCInc)[1]
		ll += ["MCIc vs MCInc (tots els 13 centres) ->(mw): "+str(estadistic)+" "+str(p_valor)]
	plt.title("All 13 centers")
	plt.xlabel("Functional Connectivity")
	plt.ylabel("kernel density estimates")
	sns.kdeplot(FC_tots_MCInc, bw=BW_GRUPALS ,shade=True, label="combined FC (MCI-nc)")
	sns.kdeplot(FC_tots_MCIc, bw=BW_GRUPALS ,shade=True, color="red", label="combined FC (MCI-c)")
	plt.savefig("fig_distFC_mitjana_TOTS_els_13centres"+str(ll_codis_centre)+".png",dpi=DPI)
	print("#######################")
	print("COMPARA DISTRIBUCIONS PER GRUP (MCI-C I MCI-nc) EN CENTRES")
	for el in ll:
		print(el)
	time.sleep(5)