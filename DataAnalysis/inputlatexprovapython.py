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