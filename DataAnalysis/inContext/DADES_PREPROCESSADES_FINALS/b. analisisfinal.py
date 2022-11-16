import os
import pandas as pd
import numpy as np
import funcions_auxiliars
import classif_pipeline_modificat as cpm
from aux__reduccio_dimensions import Analisi_components_principals as dades_acp
import aux__plot_roc_crossval as apc
import matplotlib.pyplot as plt
import time
import seaborn as sns
from scipy import stats


def crea_els_CSVs_finals_FUNCIO1():
	"""
	Aquesta funcio basicament pren les dades que haviem ja filtrat amb el document "mira_dades.py" i crea dos documents
		* out_df_final_clean.csv --> Igual que ADNIMERGE_linqueja_amb_fmri.csv però amb els UIDs afegits (per fi)
		* out_df_final_pleedeADNIMERGE.csv --> Igual que out_Df_final_clean.csv però amb totes les dades de l'amerge afegides.
	"""
	#OPEN DATAFRAME WHERE KEY VARIABLES ARE (IS OUR ALMOST DEFINTIVE SUBSAMPLE. ONLY DAYS FROM BASELINE NEED TO BE TAKEN INTO ACCOUNT TO REDUCE)
	df_casi_final = pd.read_csv("../ADNIMERGE_linqueja_amb_fmri.csv")

	#OPEN DATAFRAME WHERE ALL PHENOTIPIC DATA IS, ONLY ON BASELINES (only information we want to use).
	df_amerge = pd.read_csv("adnimerge_NOMS_VARIABLES_POSATS.csv") 
	df_amerge_bl = df_amerge[df_amerge['VISCODE'] == "bl"]; del df_amerge

	#OPEN SUBJECT IDENTIFIERS AND NEUROIMAGE IDENTIFIERS AND SAVE THEM IN ll_sub and ll_uids respectively.
	f1 = open("__subjectes.txt","r")
	f2 = open("__uids.txt","r")
	ll_sub, ll_uids = f1.read().split("\n")[:-1], f2.read().split("\n")[:-1]
	f1.close()
	f2.close()

	#CREATE DF TO ADD LL_UIDS TO df_casi_final (pd.merge es el buscarvalores de l'excel)
	df_sub_vs_uids = pd.DataFrame({"PTID":ll_sub, "UIDs":ll_uids})
	df_final_clean = pd.merge(df_casi_final, df_sub_vs_uids, how = "left", on = "PTID" , sort = False) #AFEGEIXO UIDs
	df_final_pleedeADNIMERGE = pd.merge(df_final_clean, df_amerge_bl, how = "left", on = "PTID", sort = False) #AFEGEIXO TOTES LES DADES! DESCOMENTA AQUESTA DADA PER NO OBTENIR SOROLL
	
	print(df_final_clean)
	time.sleep(2)
	#SAVE FINAL CSVs (FES SERVIR)
	df_final_clean.to_csv("out_df_final_clean.csv",sep = ",",index = False)
	df_final_pleedeADNIMERGE.to_csv("out_df_final_pleedeADNIMERGE.csv",sep = ",", index = False)




def fes_dataframe_despres_dels_3_criteris_dinclusio(desv_estandar_de_tall):
	"""
	Funcio que elimina part dels 93 subjectes segons els tres criteris d'inclusió
	que haviem decidit aplicar a l'apartat 2.3.2 Inclusion and exclusion criteria del protocol / apartat del mètode i també els d'exclusió.

	INPUT: Valor de desviació estandar a sumar a la mitjana de la distribució de temps
	que el subjecte MCI-C tarda a convertir-se, que serveix com a anys de tall per a 
	la distribució de MCI-NCs
	
	RETURNS: pandas dataframe REDUIT, 2 dataframes redundants (que tenen el mateix, pero separats epr MCI-C i MCI-NC)
	0) COMENÇO AMB EL CRITERI EXCLUSIO: is consistency will be evaluated as the absence of diagnostics that lower in severity after already having been diagnosed as rollover: i.e. if one MCI participant is later diagnosed as AD but in the next follow-up it comes back to being diagnosed as MCI or even diagnosed as Healthy the subject will be excluded.
	a) Participants that have an fMRI scan of the same submodality.
	b) Those scans will need to be within at least a \textit{$\pm 2 $ month interval} from the baseline diagnostic (a excpeció dels rollover). FA FALTA JUSTIFICAR B LA DIFERENCIA ENTRE ELS FOLLOW-UP MES PROPERS PER ALS ADNI 1 I LA EXAM DATE
	c) Among this sample, at least 80\% of the individuals need to have either CSF total, or CSF A$\beta_{1-42} $ or ADAS or MMSE scores to allow a multimodal approach according to \textbf{\textit{$H_{2}$}}. 
	d)  MCI-NC individuals must have been in a minimum of \textbf{$n$ years of a follow-up}.

		The value $n$ will be chosen by sorting in descending order
		follow-up times in MCI-NC and eliminating those subjects whose time value is below the mean time 
		of conversion for MCI-C + 1.5 standard deviations". Means and SDs come from the initial 332 MCI patient sample.
				MCI-C [time until conversion]--->  ($x$ = 2.3 years; $s$ = 1.85) --> value n calculation = 2.3 + 1.85*1 --> minimum of 4.15 years of followup 
				MCI-NC[time until loss of followup]---> ($x$ = 4.69 years; $s$ = 2.357) 
	"""
	
	df = pd.read_csv("out_df_final_pleedeADNIMERGE.csv") # --> té 93 subjectes
	
	# criterion a) 		son 93
	registres = df.shape[0]
	swap = registres
	print("criteri inclusio a:  inclosos "+str(registres)+" (d entre els 332 de la seccio de metodes).")

	# EXCLUSION CRITERION  Out of the 93 initial subjects only four present a lowering in severity after an AD diagnosis. Among those the exclusion criteria (see two definitions of "inconsistency" in the text) were applied.
	#df = df[df.PTID != '002_S_4746']	# WE DO NOT EXCLUDE HIM --> 002_S_4746 (4 consecutius de MCI (amb 2 missings entre mig). Dpesres 1 a AD i inmediatament despres de nou a MCI i depsres perdua followup. 
	df = df[df.PTID != '031_S_4005'] 	# WE MUST EXCLUDE THEM FOR TWO MCI DIAGNOSIS AFTER THE AD ONE! --> 031_S_4005 xx index 1 (12 mesos per conv)-- DOLENT -------------- (First 2 follow-ups AD. Then Goes back to MCI (2 consecutive followups corroborate the MCI and Then follow-up stops. 
	df = df[df.PTID != '019_S_4293']    # EXCLUDE THEM FOR OSCILATING PATTERN --> 019_S_4293 (24 mesos per conv) t (mci --> ad --> mci --> ad)
	df = df[df.PTID != '031_S_4947']    # EXCLUDE THEM FOR OSCILATING PATTERN -->031_S_4947 x -- POTSER DOLENT ----(MCI --> x --> AD --> MCI --> AD --> loss followup) --> varia, oscila ??

	registres = df.shape[0]
	print("criteri exclusio (inconsistencia):\n   ara queden "+str(registres)+" (dels originals "+str(swap)+" de metodes): \no sigui, "+str(swap - registres)+"exclosos.")
	
	# INCLUSION CRITERION
	#time.sleep(5)

	#criterion  b) 		Check whether at least 80 % of subjects have +- 2 months difference from bl.dx vs (examdate), EXCEPT those ADNI 1 (because dx.bl was long time ago).			
	df_no_ADNI1 = df[df["fase_estudi"] != "ADNI_1"]

	MCIc_seguits_minim_2mesos = df_no_ADNI1[df_no_ADNI1["dif_examdate_vs_dxbl"].abs() <= 60][df["s_CONVER"] == 1].shape[0]
	MCInc_seguits_minim_2mesos = df_no_ADNI1[df_no_ADNI1["dif_examdate_vs_dxbl"].abs() <= 60][df["s_CONVER"] == 0].shape[0]
	MCIc, MCInc = df_no_ADNI1[df_no_ADNI1['s_CONVER'] == 1].shape[0], df_no_ADNI1[df_no_ADNI1['s_CONVER'] == 0].shape[0]

	print("CRITERI EXCLUSIO B requereix 80% min") #NO BORREM A NINGU
	print(" percentatge MCIc amb <60 dies bl vs examdate: ", MCIc_seguits_minim_2mesos/MCIc) #90%
	print(" percentatge MCIncc amb <60 dies bl vs examdate: ", MCInc_seguits_minim_2mesos/MCInc) #91 %
	#time.sleep(2)
	
	
	# CROTERION c) 		defined below (we cut)!
	
	# STEP 1) SPLIT MCI_C and MCI_NC. 
	df_MCIc, df_MCInc = df[df['s_CONVER'] == 1], df[df['s_CONVER'] == 0] #26 MCI_C i len 67 MCI_NC respectivament
	
	# STEP 2) Delete MCI_NC with follow up times below the one defined in methods section (2.3 + 1.85 * 1 = 4.15 years of minimum follow up)
	# This is done to delete those MCI_NC who are prone to be false negatives (see -threshold n- listed and below)
	n = 2.3 + 1.85 * desv_estandar_de_tall  #YEARS THRESHOLD CUT-OFF
	df_MCInc, df_MCInc_NOINCLOSOS_PERCRITERI_C = df_MCInc[df_MCInc["DIES-SEGUIM"] > n*365.25], df_MCInc[df_MCInc["DIES-SEGUIM"] <= n*365.25]
	
	#df_MCIc = df_MCIc[df_MCIc["DIES-SEGUIM"] >= 365]  Amn aixo pots tallar els MCInc per damunt o per sota d'un temps de conversio. Empitjora la sensibilitat.
	#       REPORTING INFORMATION FOR INCLUSION CRITERION D.
	print('{:.0f} selected MCInc with follow-up time above cutoff in *years\n{:.0f} selected MCIc'.format(len(df_MCInc),len(df_MCIc)))

	print("* "+str(n)+" punt de tall -en anys- de minim follow-up assegurat per a als MCI_nc")
	print('El cutoff de n fa excloure un total de '+str(len(df_MCInc_NOINCLOSOS_PERCRITERI_C['PTID'].tolist()))+" subjectes (concretament... DESMARCACOMENTARI I MIRA "+str(df_MCInc_NOINCLOSOS_PERCRITERI_C['PTID'].tolist()))
	
	time.sleep(1)
	# STEP 3) WE CREATE a df with two keys AND ALSO A NEW CSV for analysis with other programs (such as SPSS)
	df = pd.concat([df_MCIc, df_MCInc])

	# bonus: WE ADD EXACT SUBJECT_AGES AT THE MOMENT OF ACQUIRING THE FMRI SCANS! (THEY COME FROM XML FILES )
	df_xmls = pd.read_csv("in__resum_parametres_fmri_EDATS_EXACTES_EN_MOMENTS_D'ESCANER.csv")
	df_uid_edat = df_xmls[['UIDs','AGE_ambdecimals']]
	df = pd.merge(df,df_uid_edat, how = "left", on="UIDs",sort=False)
	#bonus 2: WE WANT TO KNOW THE TIME THAT GOES FROM SCANNING TIME AND MOMENT OF END OF FOLLOW UP(MCI-NC)/CONVERSION (MCI-C). 
	# EXAM-DATE VARIABLE GIVES US THE TIME THAT GOES FROM BL.DX UNTIL END OF FOLLOUP / CONVERSION, and it is pretty informative 
	# for all participants, except those who do not belong to the ADNI 1 originally. For those DIES-SEGUIM are way too big.
	# Then we have dif_examdate_vs_dxbl, which gives us the diference examdate (scan time) vs baseline-diagnostic. 
	df['FI-FOLLOWUP-O-CONV_vs_data-escaneig'] = pd.Series((df["DIES-SEGUIM"] - df["dif_examdate_vs_dxbl"])/365.25)


	# Thus, to know the time SINCE rsfMRI scan until conversion/loss of followup for all subjects we simply need to compute the new variable
	# doing DIES-SEGUIM - dif_examdate_vs_dxbl will. NEW VARIABLE will be called ENDFOLLOW-or-CONV_vs_data-escaneig 

	#EVALUEM QUINS CENTRES HI HA 
	print("CENTRE, FREQUENCIA PER CENTRE")
	print(df["SITE"].value_counts())
	
	#EVALUEM QUINS CENTRES HI HA (GRUP MCI-C)
	print("CENTRE, FREQUENCIA PER CENTRE (MCI-c)")
	print(df["SITE"][df["s_CONVER"]==1].value_counts())
	
	#EVALUEM QUINS CENTRES HI HA (GRUP MCI-nc)
	print("CENTRE, FREQUENCIA PER CENTRE (MCI-nc)")
	print(df["SITE"][df["s_CONVER"]==0].value_counts())
	
	
	time.sleep(1)




	#guardem el df a csv 
	df["ABETA"] = df["ABETA"].replace(to_replace = ">1700", value = '1701').astype(float) #treiem primer el caracter especial superior o igual que dels valors ">1700" i ho substituim per un valor factible: 1701] cal passar a float perquè despres de la conversio tot esta en string i no se pq
	df["ABETA/PTAU"] = df["ABETA"]/df["PTAU"]	# [creem la nova variable ABETA/PTAU, que suposadament es un index que podria contribuir al diagnostic d'acord amb la lite previa (compte que no sabem si es abeta 1 42, crec que es abeta general)]
	df.to_csv("out_df_final_pleedeADNIMERGE_postcriterisInclusio.csv",sep = ",", index = False)

	#fem estadística descriptiva per variables importants dins ll_variables
	v_quantis=[('escan_vs_fi','FI-FOLLOWUP-O-CONV_vs_data-escaneig'),("AGE","AGE_ambdecimals"),("MMSE","MMSE"),("TAU","TAU"),("PTAU","PTAU"),("ABETA","ABETA"),("AB/PTAU","ABETA/PTAU"),("FDG","FDG"),("ADAS11","ADAS11"),("ADAS13","ADAS13"),("ADASQ4","ADASQ4")]#[(label_variable, nom_variable_dins_Dataframe)"}]
	v_categ = [("EMCI/LMCI","BL.dx"),("MALE/FEMALE","PTGENDER")]
	
	# criterion d) 		
		# CHECKED MANUALLY. no subjects excluded. dins els MCIc 1/23 (96%) no tenien tau, ptau o beta a. I dins els MCInc eren 3/51 (94%)
	
	#__________INFORMEM DELS NaNs__________________________
	print("\n##############################")
	print("_____NaNs per variable_______")
	for variable in v_quantis:
		label_variable, nom_variable_dins_Dataframe = variable
		nre_NaNs_a_variable = df[variable[1]].isna().values.tolist().count(True)
		print(variable[0],": ",nre_NaNs_a_variable," sobre "+str(len(df))+"({:.2f} %)".format(100*nre_NaNs_a_variable/len(df))+")") #Conto els NaNs
	time.sleep(1)

	#______Evaluem normalitat i homocedasticitat de les proves per a cada variable quantitativa en cada subgrup (MCI-C i MCI-NC) (condicions aplicacio t-test!)_________
	print("\n                SHAPIRO-WILK (NORMALITAT)          |||     levene ")
	##https://es.wikipedia.org/wiki/Test_de_Shapiro%E2%80%93Wilk |
	print("                   MCIc                 MCInc      |||   MCIc vs MCInc ")
	t_test = [] #guardo les variables que requereixen ttest. les altres fem mann whitney.
	for variable in v_quantis:
		label_variable, nom_variable_dins_Dataframe = variable
		variable_MCIc, variable_MCInc = df[nom_variable_dins_Dataframe][df['s_CONVER']==1].dropna(), df[nom_variable_dins_Dataframe][df['s_CONVER']==0].dropna()
		shapiro_MCIc, p_shapiro_MCIc = stats.shapiro(variable_MCIc);  shapiro_MCInc, p_shapiro_MCInc = stats.shapiro(variable_MCInc)
		levene_statistic, p_levene = stats.levene(variable_MCIc, variable_MCInc)
		if p_shapiro_MCIc < 0.05 or p_shapiro_MCInc < 0.05: #Si la variable NO ES NORMAL segons shapiro wilk
			if p_levene < 0.05: #si no hi ha homogeneitat de variances
				print('{:7}   {:.2f} (p = {:.5f}) | {:.2f} (p = {:.5f})* ||| {:.2f} (p = {:.3f})+[mw]'.format(label_variable,shapiro_MCIc, p_shapiro_MCIc, shapiro_MCInc, p_shapiro_MCInc, levene_statistic, p_levene))
				t_test += [False]		
			else:#si hi ha homogeneitat de variances
				print('{:7}   {:.2f} (p = {:.5f}) | {:.2f} (p = {:.5f})* ||| {:.2f} (p = {:.3f})[mw]'.format(label_variable,shapiro_MCIc, p_shapiro_MCIc, shapiro_MCInc, p_shapiro_MCInc, levene_statistic, p_levene))
				t_test += [False]
		else:#si la variable es normal segons shapiro wilk
			if p_levene < 0.05:#si no hi ha homogeneitat de variances
				print('{:7}   {:.2f} (p = {:.5f}) | {:.2f} (p = {:.5f}) ||| {:.2f} (p = {:.3f})+[mw]'.format(label_variable,shapiro_MCIc, p_shapiro_MCIc, shapiro_MCInc, p_shapiro_MCInc, levene_statistic, p_levene))
				t_test += [False]
			else: #si hi ha homogeneitat de variances
				print('{:7}   {:.2f} (p = {:.5f}) | {:.2f} (p = {:.5f})  ||| {:.2f} (p = {:.3f}) [t]'.format(label_variable,shapiro_MCIc, p_shapiro_MCIc, shapiro_MCInc, p_shapiro_MCInc, levene_statistic, p_levene))
				t_test += [True]

	print("_____________________________________________") 
	print("Ho (shapiro wilk): Poblacio del subgrup donat, per a la variabledonada, \nesta normalment distribuida. L'Asterisc surt quan refutem Ho en qualsevol dels dos grups, o sigui, quan qualsevol dels dos grups no mostra normalitat.")
	print("Ho (levene_test): els dos subgrups tenen homogeneitat de variances per a la variable donada. La creu + surt quan refutem Ho, o sigui quan no hi ha homogeneitat de variances.")
	print("[t] apareix quan la variable es susceptible de comparar-se entre grups amb t-test (exigeix homocedasticitat entre subgrups i distrib normal dins cada subgrup)")
	print("[?] Si no hi ha homogeneitat de variances pero la distribucio es normal... aleshores no se si aplicar mann whitney o t-test...")

	#__________CREEM LA TAULA 1 DE DESCRIPTIUS_____________
	print("\n      ***********************  DESCRIPTIUS  ***********************")
	print("\n#################################################################")
	print("__________MCI-C___________________MCI-NC__________valor (p-value)")
	# PRIMER VAN LES QUANTITATIVES
	for i in range(len(v_quantis)):
		variable = v_quantis[i]
		label_variable, nom_variable_dins_Dataframe = variable
		variable_MCIc, variable_MCInc = df[nom_variable_dins_Dataframe][df['s_CONVER']==1].dropna(), df[nom_variable_dins_Dataframe][df['s_CONVER']==0].dropna()
		valor_contrast_hipotesis, p_valor, boolea_t_test = funcions_auxiliars.bivariant_comparacio_mitjanes(variable_MCIc, variable_MCInc, t_test[i])
		if boolea_t_test:
			print("{:10}".format(label_variable), "{:.1f} ({:.1f})        {:.1f} ({:.1f})      {:.2f} (p = {:.5f})[t]   ".format(variable_MCIc.mean(), variable_MCIc.std(), variable_MCInc.mean(), variable_MCInc.std(),valor_contrast_hipotesis, p_valor))
		else:
			print("{:10}".format(label_variable), "{:.1f} ({:.1f})        {:.1f} ({:.1f})      {:.2f} (p = {:.5f})[mw]   ".format(variable_MCIc.mean(), variable_MCIc.std(), variable_MCInc.mean(), variable_MCInc.std(),valor_contrast_hipotesis, p_valor))
	
	#DESPRES LES CATEGORIQUES
	for variable in v_categ:
		label_variable, nom_variable_dins_Dataframe = variable
		variable_MCIc, variable_MCInc = df[nom_variable_dins_Dataframe][df['s_CONVER']==1].dropna(), df[nom_variable_dins_Dataframe][df['s_CONVER']==0].dropna()
		if label_variable == "EMCI/LMCI":
			EMCIs_MCIc, LMCIs_MCIc, EMCIs_MCInc, LMCIs_MCInc = variable_MCIc[variable_MCIc == 3].count(), variable_MCIc[variable_MCIc == 4].count(), variable_MCInc[variable_MCInc == 3].count(), variable_MCInc[variable_MCInc == 4].count()
			valor_contrast_hipotesis, p_valor = 99.99, 0.999
			print("{:10}".format(label_variable), "{:10}        {:10}    {:.2f} (p = {:.5f})[?]   ".format(str(EMCIs_MCIc)+"/"+str(LMCIs_MCIc), str(EMCIs_MCInc)+"/"+str(LMCIs_MCInc), valor_contrast_hipotesis, p_valor))
		if label_variable == "MALE/FEMALE":
			male_MCIc, female_MCIc, male_MCInc, female_MCInc = variable_MCIc[variable_MCIc == "Male"].count(), variable_MCIc[variable_MCIc == "Female"].count(), variable_MCInc[variable_MCInc == "Male"].count(), variable_MCInc[variable_MCInc == "Female"].count()
			valor_contrast_hipotesis, p_valor = 99.99, 0.999
			print("{:10}".format(label_variable), "{:10}        {:10}    {:.2f} (p = {:.5f})[?]   ".format(str(male_MCIc)+"/"+str(female_MCIc), str(male_MCInc)+"/"+str(female_MCInc), valor_contrast_hipotesis, p_valor))
	
	print("________________________________________________________________")
	print("[t] son t-test per a mostres independents. \n [mw] son Mann whitney")
	print("**COMPTE! Per a aquestes proves de comparacio de mitjanes els NaNs s'han eliminat. Diferent al que farem per al multimodal aproach, que sera mean o median imputation per a cada subgrup.")
	print("? te les odds... pero podria posar proporcions crec")
	print("________________________________________________________________")	
	print("################################################################")
	time.sleep(1)
	return df, df_MCIc, df_MCInc


def redueix_i_organitza():
	"""
	Crea labels i etiquetes. Defineix parametre de desviació estàndar per a reduir MCI-NC.
	Reorganitza 

	- arr_TS     ->  la matriu de numpy que conte les fMRIs
	- ll_sub_txt ->   fitxer txt amb els noms dels subjects
	- ll_uids  --->     fitxer txt amb els noms dels uids
	- df     ----->        pandas dataframe amb els noms dels SUIDs

	- NOTA: la funcio anterior (fes_dataframe_despres_dels_3_criteris_dinclusio()) CREA UN CSV I EL GUARDA. es igual que df, pero en csv.
	
	ORDRE CORRELATIU EN TOTS ELLS!! Cada primer element de la primera dimensió
	correspon a cada primer element dels altres 4 objectes :)
	
	"""
	df, df_MCIc, df_MCInc  = fes_dataframe_despres_dels_3_criteris_dinclusio(desv_estandar_de_tall = 0.3) #df amb totes les dades --> 0.5 OBTE 70 SUB | 1 OBTE 57 | 0.3 obte X pero te la millor accuracy
	
	print(str((df["FI-FOLLOWUP-O-CONV_vs_data-escaneig"][df["s_CONVER"]==0].min()))+" subjecte MCI-nc despres del cuttoff a 2.8 anys\n amb menys temps de followup")
	time.sleep(3)
	arr_TS = np.load("__arr_ADNI_3d_preprocessada.npy") #--> [93,214,140] --> [subjectes, ROIs, TS] 
	#funcions_auxiliars.comprova_nans(arr_TS) --> matriu 3D esta perfecta!!
	f1 = open("__subjectes.txt","r") 
	f2 = open("__uids.txt","r")
	ll_sub_txt, ll_uids = f1.read().split("\n")[:-1], f2.read().split("\n")[:-1] #len 93 (ORDRE CORRELATIU A PRIMERA DIMENSIO arr_TS, conte subjects IDs).
	f1.close()
	f2.close()
	
	#compte perque ll_sub_txt i la primera dimensio de l'array de numpy estan ordenats, pero no pas el df. A part, cal eliminar els indexos que no volem a l'analisis perqueels hem exclos abans!	 
	#PAS 1) CERCO INDEXOS PER A LA PRIMERA DIMENSIÓ DE L'ARRAY DE NUMPY (STACK MATRIUS, 93) QUE ES TROBIN A LA COLUMNA PTID del dataframe.
	ll_MCI_df = df["PTID"].tolist()
	ll_indexos_a_retenir = [] #indexos de l'array de numpy qeu em vull quedar per analitzar
	for subjecte_id in ll_MCI_df:
		ll_indexos_a_retenir += [ll_sub_txt.index(subjecte_id)]
	
	#PAS 2) FAIG SERVIR AQUESTS INDEXOS QUE HE DE RETENIR PER A DIR QUE EM BORRI 
	# ELS INDEXOS QUE NO HE DE RETENIR  (MITJANÇANT UNA DIFERENCIA DE CONJUNTS NORMAL I CORRENT)
	ll_indexos_total = list(range(len(ll_sub_txt)))
	for index_retenir in ll_indexos_a_retenir:
		del ll_indexos_total[ll_indexos_total.index(index_retenir)]
	#print(len(ll_indexos_total)+len(ll_indexos_a_retenir) == 93); print(ll_indexos_total); print(len(ll_indexos_a_retenir)) #len 57, correcte
	
	#DEIXEM NOMES ELS 57 SUBJECTES SELECCIONATS, TANT A L'ARRAY arr_TS COM A LA LLISTA ll_sub_txt
	arr_TS = np.delete(arr_TS,ll_indexos_total,axis=0); print(arr_TS.shape) #(57,214,140) :)
	ll_s = []
	ll_u = []
	for index in ll_indexos_a_retenir:
		ll_s += [ll_sub_txt[index]]
		ll_u += [ll_uids[index]]
	ll_sub_txt = ll_s[:]; del ll_s #ll_sub_txt te len 57 :)
	ll_uids = ll_u[:]; del ll_u
	np.save("out_arr_TS_final ("+str(len(arr_TS))+" subjectes)", arr_TS)
	df = df.loc[df['PTID'].isin(ll_sub_txt)] #selecciono noms dels 57 subjectes 
	print("Tots han de ser iguals ---> ",len(ll_uids),len(ll_sub_txt),len(arr_TS),len(df))
	time.sleep(1)
	return arr_TS, ll_sub_txt, ll_uids, df #TORNEM LO MATEIX PERO ARREGLAT I reduit
		
	
	
def mat_corr_labels_i_pipeline(ploteja_totes_les_matrius_de_conectivitat, ploteja_una_matriu_de_conectivitat_mitjana_per_cada_grup, ploteja_funcions_densitat_probabilitat_FCON_per_centre):
	"""
	arr_TS, ll_sub_txt, ll_uids i df tenen dimensions correlatives.
	"""
	t1 = time.clock()
	arr_TS, ll_sub_txt, ll_uids, df = redueix_i_organitza() #arr_TS --> (57,214,140)  (SUB, ROI, TS)
	arr_TS = np.transpose(arr_TS,(0,2,1)) # --> arr_TS ara te shape (57,140,214)  (SUB, TS, ROI)
	

	#CREO VARIABLE arr_corr, que contindrà un stack de matrius de correlacions (tantes com subjectes)
	arr_corr = []
	for i in range(len(arr_TS)): 
		ll_arr_corr = pd.DataFrame(arr_TS[i]).corr().values.tolist() #ll_ARR_CORR --> (214,214)) --> faig pas DF --> NDARRAY --> LIST per poder fer l'stack bé (no se com fer-ho en numpy)
		arr_corr += [ll_arr_corr]
	arr_corr = np.array(arr_corr) # shape (57,214,214) (Shape pot canviar en funcio del parametre de desviacio tipica, recorda)
	np.save("out_FC ("+str(len(arr_corr))+" subjectes)", arr_TS)
	print("arr_corr shape", arr_corr.shape)

	if ploteja_totes_les_matrius_de_conectivitat:#si vols les 93 no has de tallar la distribucio (posa valor arbitrariament negatiu i molt petit (-6 p ex) a la variable "desv_estandar_de_tall")
		nom_directori_guardar_ROIxROI = "les_submatrius_finalment_analitzades"
		for i in range(len(arr_corr)): 
			if df["s_CONVER"].values[i]== 1:
				categoria, missatge_dies = "MCIc", " months to AD conversion"
			else: #cas 0
				categoria, missatge_dies  = "MCInc"," months follow-up"
			dies_seg = str(df["DIES-SEGUIM"].values[i])
			titol_grafic_guardat = categoria+"_"+"mesosSeg_"+str(int(dies_seg)//30)+"_"+ll_sub_txt[i]+"_"+ll_uids[i]+"index arr_corr__"+str(i)
			titol_figura = categoria+"  "+ll_sub_txt[i]+" | "+str(int(dies_seg)//30)+missatge_dies  #ojo que els he truncat, no arrodonit
			#plt.matshow(arr_corr[i])

			f, ax = plt.subplots(figsize=(11, 9))
			plt.title(titol_figura)
			cmap = sns.diverging_palette(220, 10, as_cmap=True)			# Generate a custom diverging colormap
			sns.heatmap(arr_corr[i], cmap=cmap, vmax=1, center=0, square=True, linewidths=.0, cbar_kws={"shrink": .5}) # Draw the heatmap with correct aspect ratio
			plt.savefig('./'+nom_directori_guardar_ROIxROI+'/'+titol_grafic_guardat+".png")

	if ploteja_una_matriu_de_conectivitat_mitjana_per_cada_grup:
		ll_indexos_MCIc = []
		ll_indexos_MCInc = []
		for i in range(len(arr_corr)): 
			if df["s_CONVER"].values[i]== 1:
				ll_indexos_MCIc += [i]
			else: #cas 0
				ll_indexos_MCInc += [i]
		print("INDEXOS MCIc",len(ll_indexos_MCIc))
		print("INDEXOS MCInc",len(ll_indexos_MCInc))
		time.sleep(2)
		print(ll_indexos_MCIc)
		time.sleep(1)
		matriu_corr_mitjana_MCIc = funcions_auxiliars.mitjana_stack_element_wise(arr_corr[ll_indexos_MCIc,:,:]) #poso nomes les matrius dels MCIc per a fer la mitjana
		matriu_corr_mitjana_MCInc = funcions_auxiliars.mitjana_stack_element_wise(arr_corr[ll_indexos_MCInc,:,:]) #poso nomes les matrius dels MCInc per a fer la mitjana
		
		f, ax = plt.subplots(figsize=(11, 9))
		plt.title("fc matrix (MCI-nc group)")
		cmap = sns.diverging_palette(220, 10, as_cmap=True)			# Generate a custom diverging colormap
		sns.heatmap(matriu_corr_mitjana_MCInc, cmap=cmap, vmax=1, center=0, square=True, linewidths=.0, cbar_kws={"shrink": .5}) # Draw the heatmap with correct aspect ratio
		plt.show()
		#f.savefig('fig_matriu_corr_mitjana_MCInc.svg', format='svg', dpi=1200)
		plt.close()

		f, ax = plt.subplots(figsize=(11, 9))
		plt.title("fc matrix (MCI-c group)")
		cmap = sns.diverging_palette(220, 10, as_cmap=True)			# Generate a custom diverging colormap
		sns.heatmap(matriu_corr_mitjana_MCIc, cmap=cmap, vmax=1, center=0, square=True, linewidths=.0, cbar_kws={"shrink": .5}) # Draw the heatmap with correct aspect ratio
		plt.show()
		#f.savefig('fig_matriu_corr_mitjana_MCIc.svg', format='svg', dpi=1200)
		plt.close()


	#CREO VARIABLE X per a a fer ML. X conté la F.Connectivity vectoritzada, o sigui conté
	#CADA MATRIU DE l'stac arr corr queda vectoritzada i guardada com a matriu 2D 
	X = [] 
	for i in range(len(arr_corr)):
		ll_vector = funcions_auxiliars.elimina_tri_superior_i_flateneja_ROIxROI(arr_corr[i])
		X += [ll_vector] 
	
	#FAIG GRAFIC DE LES PDFs per a les FCON vectoritzades PER centre. Aixi comparo si surten diferents per centre.
	if ploteja_funcions_densitat_probabilitat_FCON_per_centre:
		funcions_auxiliars.plot_pdf_FC_centres(FC_vectoritzada=np.array(X),
											   ll_codis_centre=[1,53,22],
											   df=df) #SON ELS 3 CENTRES (CODIS variable SITE del dataframe) que aporten mes pacients

	#FAIG LA CONNECTIVITAT FUNCIONAL VECTORITZARDA ARRAY DE NUMPY
	X = np.array(X); print("X shape: ", X.shape) 

	#PROVO_DIVERSOS_CLASSIFICADORS (SI TOTS ESTAN A FALSE CLASSIFICA PER LA CONECTIVITAT FUNCIONAL. En cas contrari, no.)
	classifica_NOMES_per_edat, classifica_NOMES_per_biomarcadors, classifica_NOMES_per_questionaris = False, False, False
	#####################################
	if  classifica_NOMES_per_edat:
		X = df["AGE"].values.reshape(-1,1); print("X shape: [ACTIVAT MODEL DE CLASSIFICACIO PER EDAT I NO FMRI]", X.shape)
		time.sleep(3)
	if classifica_NOMES_per_biomarcadors:
		X = df["ABETA/PTAU"].values.reshape(-1,1); print("X shape: [ACTIVAT MODEL DE CLASSIFICACIO PER ABETA/PTAU I NO FMRI]", X.shape)
		time.sleep(3)
	if classifica_NOMES_per_questionaris:
		X = df[["ADAS11", "ADAS13","ADASQ4"]].values; print("X shape: [ACTIVAT MODEL DE CLASSIFICACIO PER ADAS I NO FMRI]", X.shape)
		time.sleep(3)
		#ADAS11 SOL PERFECTE
	#CREO VARIABLE Y, que contindrà les labels (1 --> MCI-C | 0 --> MCI-NC)	 	
	Y = df["s_CONVER"].values;	print("Y shape: ", Y.shape) # Y te shape (57,)
	print("Y shape: ",Y.shape) 
	time.sleep(2)
	
	
	#ANALISI INDEPENDENT 2)  FEM 10-fold-crossvalidation + SVM --> RESULTATS MOLT POBRES AMB PCA, tant estandaritzant com sense fer-ho. No diagnostica cap malalt, specificiat 0 amb PCA. probats varis components
	apc.PCA_10foldCV_ROC(X=X, 
						 y=Y,					# NOTA_ PCA_by_santi i rfecv son mutuament excloents
						 PCA_by_santi=False, 	# primer boolea True si vols fer PCA (false si no el fas)#Si vols estandaritzar columnes en fer el PCA (Si no el fas es igual si es True o false)has d'anar a dins el fitxer i buscar "estandaritzar_variables"
						 rfecv=False,  			# no funciona... si poses True hauria de fer Recursive feature elimination. Si poses False no te la fa
						 fes_violin_plot_accuracies_per_folds_i_classificador=True,
						 carpeta='BIOMARCADORS_models_finals')	# SI TOQUES COSES DE fMRI treu-ho a la carpeta 'fMRI_models_finals'

						 #NOTA: LA CARPETA ON GUARDARAS TOTES LES ACCURACY METRICS. Ha d'existir primer o dona error.


	
#crea_els_CSVs_finals_FUNCIO1()
mat_corr_labels_i_pipeline(ploteja_totes_les_matrius_de_conectivitat = False,
						   ploteja_una_matriu_de_conectivitat_mitjana_per_cada_grup = False, 
						   ploteja_funcions_densitat_probabilitat_FCON_per_centre = True)

#NOTA SI VOLS LES CONFUSION MATRIX PRIMER EXECUTA LA FUNCIO mat_corr_labels_i_pipelines i NOMES DESPRES
#desactiva mat_corr_labels i crida grafiqueja_confusions_matrix




###################################################

def grafiqueja_confusions_matrix(fontsize):
	"""
	QUE FA? PLOTEJA TOTES LES ARRAYS DE NUMPY DE LA CARPETA DONADA EN HEATMAP. 
	LES ARRAYS QUE HI HA ALLI SON CONFUSION MATRIX DELS CLASSIFICADORS.

	Xucla TOTES les .npy guardades a la carpeta d'exportacio fMRI_models_finals i en fa plots de heatmap. 
	#####   Genera una --> ESCALA DE MAPA DE CALOR COMUNA<---- a tots ells  #######
	Ho fa prenent el valor maxim de totes les arrays i el valor minim i els utilitza com a limits superior i inferior
	del heatmap respectivament. Aixi permet comparar entre tots els heatmaps de la carpeta. Cal posar-los, doncs, junts al treball.

	NOTA: el titol de l'array el pren a partir d'un split "__" per tant el que surt a la dreta de "__" SERA EL NOM DE CADA TITOL.
	"""
	os.chdir("."+os.sep+"fMRI_models_finals")
	stack_confusions_matrix = []
	noms_classificadors = []
	for fitxer in os.listdir(os.getcwd()):
		if ".npy" in fitxer:
			stack_confusions_matrix += [np.load(fitxer)]
			noms_classificadors += [fitxer.split("__")[1].split(".")[0]] 

	arr_confusions_matrix = np.array(stack_confusions_matrix); del stack_confusions_matrix
	vmin_heatmap, vmax_heatmap = arr_confusions_matrix.min(), arr_confusions_matrix.max()
	for i in range(len(arr_confusions_matrix)):
		confusion_matrix = arr_confusions_matrix[i]
		df_cm = pd.DataFrame(confusion_matrix, index=["+ test","- test"], columns=["MCI-c", "MCI-nc"])
		fig = plt.figure(figsize=(10,7))
		heatmap = sns.heatmap(df_cm, annot=True, fmt="d", vmin=vmin_heatmap ,vmax=vmax_heatmap)
		heatmap.yaxis.set_ticklabels(heatmap.yaxis.get_ticklabels(), rotation=90, ha='right', fontsize=fontsize)
		heatmap.xaxis.set_ticklabels(heatmap.xaxis.get_ticklabels(), rotation=0, ha='right', fontsize=fontsize)
		nom_classificador = noms_classificadors[i]
		plt.title(nom_classificador)
		plt.xlabel('True outcome')
		plt.ylabel('Predicted outcome')
		plt.show()
            
	os.chdir("../")

#grafiqueja_confusions_matrix(20)