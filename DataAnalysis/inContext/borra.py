import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv("ADNI_tots_fMRI_tots_2_13_2018.csv")
freq_modalitats_fMRI = df["Description"].value_counts()

"""
EL GRÀFIC I EL PRINT DE SOTA ENS MOSTREN QUE HI HA 
7 MODALITATS FORÇA FREQUENTS DINS DE LES ADQUISICIONS DE FMRI
DE TOT EL ADNI. ENS INTERESSA RESTING STATE FMRI

MoCoSeries                                                          1683
relCBF                                                              1676
Perfusion_Weighted                                                  1668
ASL PERFUSION                                                       1211
Resting State fMRI                                                   770
ASL_PERFUSION                                                        294
Axial rsfMRI (Eyes Open)                                             199
Extended Resting State fMRI                                          129
"""

plt.plot(list(freq_modalitats_fMRI), 'ro')
plt.xlabel("ordre_llista_ordenada")
plt.ylabel("nombre d'scans")
print(freq_modalitats_fMRI)