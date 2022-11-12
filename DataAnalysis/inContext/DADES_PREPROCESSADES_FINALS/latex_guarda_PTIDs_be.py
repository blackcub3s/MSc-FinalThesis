#!/usr/bin/env python
# -*- coding: utf-8 -*-

def posa_barres_latex(ll_PTIDs):
	for i in range(len(ll_PTIDs)):
		snou = ''
		for caracter in ll_PTIDs[i]:
			if caracter == "_":
				snou = snou + "\_"
			else:
				snou = snou + caracter
		ll_PTIDs[i] = snou
	with open("sortida_exclosos_criteri_c.txt","w") as f:
		f.write(str(ll_PTIDs))



posa_barres_latex(['002_S_2043', '018_S_2138', '013_S_2324', '129_S_4073', '002_S_4237', '019_S_4285', '130_S_4468', '136_S_4517', '013_S_4791', '031_S_4194','002_S_4219', '002_S_4251', '136_S_4408', '130_S_4605', '130_S_4925', '013_S_4985'])