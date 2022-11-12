# -*- coding: utf-8 -*-
"""
Created on Mon May 28 04:24:13 2018

@author: santi
"""

import pandas as pd
from scipy.stats import ttest_ind
from matplotlib import pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats
import matplotlib
matplotlib.use('Agg')
def separa_distribucions_MCIC_vs_MCINC():
	"""
	Calcul per a la regió del text amb cita literal "is clearly below MCI-NC time of follow-up(
	"""
	df = pd.read_csv("ADNIMERGE_sortida.csv")
	seguim_MCI_c, seguim_MCI_nc = df["DIES-SEGUIM"][df["s_CONVER"]==1], df["DIES-SEGUIM"][df["s_CONVER"]==0]
	print ("years from from DX.bl until conversion (MCI_C):")
	print("{:.3f} years".format(seguim_MCI_c.mean()/365.25),"(std = {:.3f})".format(seguim_MCI_c.std()/365.25))	
	print("")
	print("years from DX.bl until follow up stop (MCI_nc)")
	print("{:.3f} years".format(seguim_MCI_nc.mean()/365.25),"(std = {:.3f})".format(seguim_MCI_nc.std()/365.25))	

	print("\nt-test:\n ", ttest_ind(seguim_MCI_c, seguim_MCI_nc))
	
	df.stack()
	#ULTIMA COLUMNA TRANSOFORMADA A ANYS
	print(df,df["DIES-SEGUIM"]/365.25)
	arr_anysMCIc, arr_anysMCInc = (seguim_MCI_c/365.25).as_matrix(),(seguim_MCI_nc/365.25).as_matrix()
	sns.distplot(arr_anysMCIc, bins=5, kde=True, rug=True);
	sns.distplot(arr_anysMCInc, bins=5, kde=True, rug=True);	
	
	#sns.distplot(arr_anysMCIc, kde=True, fit=stats.gamma);
	#sns.distplot(arr_anysMCInc, kde=True, fit=stats.gamma);	
	#plt.show()

separa_distribucions_MCIC_vs_MCINC()