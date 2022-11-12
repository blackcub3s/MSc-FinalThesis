#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
from sklearn.decomposition import PCA
from sklearn import preprocessing
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from string import ascii_letters



class Grafics:
	"""
	Classe que pren una matriu 2D i la ploteja.
	"""
	def __init__(self,matriudades):
		self.d = matriudades
	def grafic_correlacions_seaborn(self):
		"""
		CODI ADAPTAT DE https://seaborn.pydata.org/examples/many_pairwise_correlations.html
		Serveix per fer un grafic de una matriu de correlacions.

		crido aquesta funció dins la classe Analisi_components_principals, mètode matriu_correlacions
		"""
		sns.set(style="white")

		# Generate a large random dataset
		#rs = np.random.RandomState(33)
		#d = pd.DataFrame(data=rs.normal(size=(100, 26)),
		#                 columns=list(ascii_letters[26:]))

		# Compute the correlation matrix
		corr = self.d  #aqui self.d conté la matriu de correlacions perquè cridem aquesta funció des de metode matriu_correlacions.	

		# Generate a mask for the upper triangle
		mask = np.zeros_like(corr, dtype=np.bool)
		mask[np.triu_indices_from(mask)] = True

		# Set up the matplotlib figure
		f, ax = plt.subplots(figsize=(8, 5))

		# Generate a custom diverging colormap
		cmap = sns.diverging_palette(220, 10, as_cmap=True)

		# Draw the heatmap with the mask and correct aspect ratio
		sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3, center=0,
		            square=True, linewidths=.5, cbar_kws={"shrink": .5})		


class Analisi_components_principals:
	"""
	Classe que permet implementar tots els passos per realitzar un anàlisis de components principals a partir d'una matriu de dades 2D
	de shape (n_samples,n_features) o, en altres paraules, (nombre_subjectes a files, nombre variables d'entrada a columnes).
	Compte, perquè no admet pas inputs de matrius 3D o ordes superiors.

	Els passos que se segueixen en aquesta classe queden ben resumits en aquest tutorial
	de SPSS: http://bit.ly/2rJfRtR.

	PARÀMETRES: - Matriu de dades
	            - nombre_components --> int --> Quants components a retenir (comença amb None -els reté tots- i tu has d'acabar escollint-ne el mínim raonable).
				- estandaritza_variables --> bool --> si TRUE el que fa es estandaritzar cada columna (variable) a distribucio de mitjana 0 i dt=1.
	
	MÈTODES:     
				- matriu_correlacions()
				- testeja_esfericitat() --> Impossible definir-lo amb info online. Buscar bé!
				- autovalors_i_variansssa()
				- puntuacions_factorials()
	
	RETURN MÉS IMPORTANT: El que dóna puntuacions_factorials()):
				- n.darray de "dimensionalitat" reduida (puntuacions_factorials(): 
	
	"""
	#DEFINEIXO, PER A TOTES LES FUNCIONS DE LA CLASSE, EL FORMATEIG DE SORTIDA DELS NOMBRES DE LES ARRAYS DE NUMPY.
	# NOTA: NO CANVIA LA PRECISIÓ AMB LA QUE ES FAN CALCULS NI AMB LA QUE ES RETORNEN VALORS (NOMÉS FORMATEJA ELS PRINTS CALLS)
	# https://stackoverflow.com/questions/21008858/formatting-floats-in-a-numpy-array/21008904
	np.set_printoptions(formatter={'float': '{: 0.3f}'.format})

	def __init__(self,matriu_dades,nombre_components, estandaritza_variables,llista_variables):
		"""
		Explicat a sota la classe.
		"""
		self.M = matriu_dades
		self.nombre_components = nombre_components
		
		#passo la llista de variables, si es que n'hi ha, com un argument OPCIONAL de tipus llista.
		self.llista_variables = llista_variables

		#estandaritzo cada variable (cada columna) a distribució mitjana 0 i desviació típica 1. Importantíssim!
		if estandaritza_variables:
			self.M = preprocessing.scale(self.M)
			

		# Implemento PCA a partir de http://bit.ly/2yGcFNP (Les dues linies seguents s'haguessin pogut ometre, però així ho entenc més)
		n_mostres = len(self.M) #nombre files matriu
		n_variables_entrada = len(self.M[0]) #nombre columnes matriu

		if self.nombre_components==None:
			pca = PCA(n_components = min(n_mostres,n_variables_entrada)) #si posaves none crec que anava igual
			pca.fit(self.M)
		else:
			pca = PCA(n_components = self.nombre_components)
			pca.fit(self.M)
		self.pca = pca
	
	def matriu_correlacions(self, grafic_correlacions):
		"""
		Retorna la matriu de correlacions entre les variables del dataframe (cols) i els casos (files).
		Si grafic_correlacions=True fa el gràfic
		"""
		
		# SI LLISTA_vARIABLES ESTÀ BUIDA, NO MIRO RES I FAIG EL GRAFIC DIRECTAMENT (AMB ETIQUETES DEFAULT).
		# EN CAS CONTRARI ALESHORES COMPROVO SI LA LLISTA DE NOMS DE VARIABLES (PER A ETIQUETES DEL PLOT DE CORRELACONS)
		# COINCIDEIX, EN NOMBRE, AMB EL NOMBRE TOTAL DE VARIABLES. SI COINCIDEIX FAIG EL GRÀFIC,
		# EN CAS CONTRARI, POSO UN ERROR.
		if len(self.llista_variables) != 0:
			if len(self.llista_variables) < len(self.M[0]):
				raise ValueError("Has introduit menys noms de\nvariables (strings) al parametre llista_variables \nque variables tens a la matriu (columnes)... \nFalta/en strings de nom/s de variable!")				
			elif len(self.llista_variables) > len(self.M[0]):
				raise ValueError("Has introduit mes noms de\nvariables (strings) al parametre llista_variables \nque variables tens a la matriu (columnes)... \nSobra/en strings per a nom/s de variables")				
			else: #CAS EN QUE COINCIDEIXEN I EN QUE POTS FER B EL GRÀFIC
				ll = self.llista_variables
				matriu_dades_pandas = pd.DataFrame(data = self.M, columns = self.llista_variables)
		else:
			matriu_dades_pandas = pd.DataFrame(data = self.M)
		
		#FAIG LA MATRIU DE CORRELACIONS
		mat_correl_pearson = matriu_dades_pandas.corr()
		if grafic_correlacions:
			#mostra grafic guay de seaborn_DEFINIT A LA CLASSE GRAFICS
			Grafics(mat_correl_pearson).grafic_correlacions_seaborn()
			plt.show()
		print("---matriu de correlacions entre variables----\n(abans de fer cap reduccio de dimensio)")
		print(mat_correl_pearson)
		return mat_correl_pearson


	def testeja_esfericitat(self,Bartlett,KMO):
		"""
		Returns: String amb el p valor de la prova que comprova l'esfericitat de la matriu mitjançant la Prova d'esfericitat de bartlett i/o  algo de la 
		prova de kaiser-meyer-olkin. NOTA: Abans de fer PCA i testejar l'esfericitat, sempre cal inspeccionar visualment la matriu de 
		correlacions.

		Paràmetres: 2 booleans.

		Aquesta funció nira si la matriu de correlacions té proutes correlacions que realment difereixen de 0. Això es pot fer amb la prova d'esfericitat
		de bartlett (1951) o bé amb la prova KMO, que són les que implementa aquesta funció. Per cridar una, l'altra, o ambdues
		posem True o False segons correspongui als paràmetres "Bartlett, KMO.
		
		Per què ho fem?

		Ho fem perquè la matriu de correlacions observada en la nostra mostra sobre la que es basa l'ACP ha de ser estadísticament diferent 
		(a nivell poblacional) a la matriu identitat o a la matriu de 0 correlacions. Això és així perqupe L'ACP
		requereix tenir algunes variables que estiguin correlacionades entre sí per tal de crear uns components que en recullin la seva variabilitat
		i que, alhora, estiguin descorrelacionats (ortogonals). Si no hi hagués correlacions entre CAP d'aquestes variables (i.e la matriu de correlacions
		no fos diferent a la matriu identitat) aleshores no tindria sentit aplicar un ACP per reduir dimensionalitat (ni tan sols 
		per descorrelacionar dades en comptes de reduir dimensionalitat).

		"""		

		# No hem pogut implementar-les.
		# contribueix
		# https://github.com/statsmodels/statsmodels/blob/master/CONTRIBUTING.rst"""
		if Bartlett:
			#NINGU L'HA DEFINIT A SCYPY... teoricament ho vol fer aquest però no s'ha fet... https://groups.google.com/forum/#!topic/pystatsmodels/B61oAHWP8S8
			#A L'R I L'SPSS SÍ QUE HI SON. L'HE INTENTAT DEFINIR SEGONS AIXÒ PER
			# PERÒ NO EM QUEDA CLAR QUÈ ÉS EL VALOR p DELS ARGUMENTS... ' https://personality-project.org/r/html/cortest.bartlett.html. 
			# MIRA LA BIB ORIGINAL BARTLETT(1951) + spss
			#esfericitat_bartlett = -math.log(np.linalg.det(self.M)*   	)
			pass
		if KMO:
			pass #NINGU L'HA DEFINIT... fesho per a les dues proves. 
	
	def autovalors_i_variansssa(self, scree_plot):
		"""	Obten una taula d'autovalors (EIGENVALUES) i de variances explicades per component per a un nombre 
		    donat de components (self.nombre_components). Si scree_plot es True en fa l'scree plot de tants components com nombre_components tens. Això és el que
			ens permet prendre decisions sobre decidir si retenir o no retenir compoennts.

			Si self.nombre_components = None imprimeix en pantalla tots els components retornables.
			_________________________
			Com prendre decisió? Hi ha diversos criteris:

			CRITERI 1 (més acceptat): Retingues un nombre de components abans del colze a l'scree plot (equilibri entre variança explicada pel model i
			model parsimoniós amb pocs components)

			CRITERI 2 (poc acceptat té flaws): Retingues tants components com autovalors (eigenvalues) superiors a 1.
		"""





		#torna els EIGENVALUES -autovalores o valors propis- dels nombre_components demanats [shape: (nombre_components,1)]
		ll_valors_propis = self.pca.explained_variance_

		#torna els percentatge de variança explicada per cada component del nombre_de_components demanats [shape: (nombre_components,1)]:
		ll_variansssa_explicada_per_component = self.pca.explained_variance_ratio_

		#fes una taula xula per visualitzar els eigenvalues i la variança explicada per component
		taula_str_print = '\n\ncomponent    valor_propi     variansssa_explicada_per_component (tant per cent)\n'
		ll_components = [] #guardo l'index per fer el scree_plot despres
		for i in range(len(ll_valors_propis)):
			ll_components = ll_components + [i+1]
			taula_str_print = taula_str_print+"   "+str(i+1)+'       '+'{:10.2f}'.format(ll_valors_propis[i])+'           '+'{:10.2f}'.format(ll_variansssa_explicada_per_component[i]*100)+'\n'
		variansa_acumulada = "{:.2f}".format(sum(ll_variansssa_explicada_per_component)*100)
		taula_str_print = taula_str_print + "\n**** Varianssa de les dades\nexplicada amb "+str(len(ll_components))+ 'retinguts: '+variansa_acumulada
		#l'imprimim en pantalla i també la guardem en un .txt
		
		print(taula_str_print)
		with open("eigenvalues_i_variansssa_Explicada.txt","w") as f:
			f.write(taula_str_print)

		#fem el gràfic (si l'hem demanat)
		if scree_plot==True:
			plt.plot(ll_components,ll_valors_propis,"or-")
			plt.plot([1,ll_components[len(ll_components)-1]], [1,1],"b-") #fem scree_plot possible linia orientativa de criteri de decisio 1 (veure docstring)
			plt.title("scree plot")
			plt.xlabel("components retinguts")
			plt.ylabel("valors propis (eigenvalues)")
			plt.show()
		
		#return valors_propis, variansssa_explicada_per_component

	def carregues_factorials(self):
		"""les carregues factorials o FACTORIAL LOADINGS et mostren la correlació de cada VARIABLE o FEATURE amb cada component. 
		   Per tant, t'ajuden a aconseguir dues coses:
		   		1 --> interpretar el significat de cada component: com feiem a psicologia
				2 --> calcular les puntuacions de cada subjecte a cada factor
		"""
		#shape (n_components, n_features) 
		carregues_factorials = self.pca.components_   			
		
		#shape(n_features, n_components)
		carregues_factorials_transposades = np.transpose(carregues_factorials)
		self.A = carregues_factorials_transposades  #veure funcio "puntuacions_factorials" per a entendre-ho
		
		print("\n--------CARREGUES FACTORIALS (correlacions variables entrada vs components)--")
		print("   components de 1 a "+str(len(carregues_factorials_transposades[0]))+" en columnes (d'esquerra a dreta)")	
		print(carregues_factorials_transposades)
		print("** Features o variables d'entrada estan a files!! A files\nno hi ha subjectes aqui")
		#return carregues_factorials_transposades 

	def puntuacions_factorials(self, imprimeix_dataset_reduit):
		"""
		Return:   el dataset reduit!!! A columnes tens els factors (components), i a files tens les 
		          puntuacions de cada subjecte o cas, per a cada factor (component). Estpa Llest per introduir 
		          a un model d'aprenentatge automàtic i evitar l'overfitting, sempre que hagis reduit prou les dades!

		parametres: Només un. Booleà. --> si volem imprimir en pantalla el dataset reduit o no.

		EXPLICACIÓ:

		Les puntuacions cada subjecte (fila de la matriu d'entrada de dades), en el nou espai de p components, 
		es calculen multiplicant cada vector de carregues factorials (un per cada component) per la puntuació de cada subjecte en cada 
		feature o variable d'entrada. Cada subjecte té, doncs, una sola puntuació per factor o component.

		Per tal de fer-ho per a tots cal fer una multiplicació de  

		Si tinc una matriu de dades M de dimensions m x n (on m son files: nre persones, casos...; i n son columnes: nombre de features)
		i he d'obtenir una matriu M' de features reduides en p components (és a dir m x p) aleshores he de trobar una matriu A tal que:

																M * A = M'

		Per tant, A tindrà tantes columnes com la matriu M i tantes files com la matriu M'. A tindrà doncs shape (m x p), és a dir, 
		A tindrà m nombre persones, casos (a files) i els p COMPONENTS a columnes.

		La matriu "carrega_factorial_transposades que retorna la funció anterior es precisament la que volem com a matriu A. 

		NOTA: M' ES DIRÀ DATASET REDUIT "
		NOTA: EL dataset reduit es podia haver obtingut de fomra molt més senzilla, invocant el mètode 
		self.pca.transform(self.M), que dona exactament el mateix que el calcul fet amb la multiplicació.


		"""
		#FEM EL CÀLCUL MENCIONAT AL DOC STRING
		dataset_reduit = np.matmul(self.M,self.A)
		#dataset_reduit = self.pca.transform(self.M)

		#IMPRIMIM LA MATRIU DE DADES REDUIDA (SI ES DEMANA A LA FUNCIÓ)
		if imprimeix_dataset_reduit:
			print('\n\n--------PUNTUACIONS FACTORIALS (DATASET REDUIT EN COMPONENTS)--------')
			print(dataset_reduit)
			print("*** files tenen els subjectes, casos. Això és el que entra al model!!!!\n Components estan en columnes")
			#print(self.pca.transform(self.M))
		#aixo anirà a un model d'aprenentatge automàtic
		return dataset_reduit 


# nombre components = None si vols que els torni tots. 
# estandaritza_variables = True si vols estandaritzar (indispensable). 

												#"a","b","c","d",[...]
dades = Analisi_components_principals(np.array([[60,70,32,10,13,14,12],
							  					[80,90,95,20,27,8,11],
							  					[62,71,65,13,14,15,19],
							  					[90,70,60,15,22,6,13],
							  					[85,75,60,14,10,9,14]],dtype=np.float64),
												nombre_components = None, 
												estandaritza_variables = True,
												llista_variables=['a','b','c','d','e','f',"G"])  #POTS DEIXAR LA LLISTA BUIDA, PERO MANTENINT-LA!!

 


dades.matriu_correlacions(grafic_correlacions=True)  # ACP es basa en la matriu de corr. davant absencia de proves de esfericitat (bartlett,KMO) es importantissim mirar que la matriu de correlacions no s'apropa a la matriu identitat. Volem variables correlacionades o no te sentit aplicar PCA
dades.autovalors_i_variansssa(scree_plot=True)       # veure autovalors, variança explicada i screeplot. Amb això (especialment amb l'screeplot), decideix quants components retenir combinant variança explicada i parsimònia.
dades.carregues_factorials()						 # veure les correlacions entre cada factor i cada variable
dataset_reduit = dades.puntuacions_factorials(imprimeix_dataset_reduit = True) # METODE QUE RETONRA EL DATAET REDUIT. ndarray reduit!

# POSA dataset_reduit A UN MODEL!!!! I VINGA!!!

# NOTES: despres d'estandaritzar, les variançes explicades dels components QUadren a la perfeccio amb spss. 
# Per tant, els eigenvalues, encara que no quadren, està ok. No entenc per què les carregues factorials i les punfuacions factorials 
# no coincideixen amb l'SPSS. SERÀ QUE IMPLEMENTEN UN MÈTODE DIFERENT?

