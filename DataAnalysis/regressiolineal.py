import matplotlib.pyplot as plt
import numpy as np
import scipy.stats
import math

#PRE: l'arxiu dades té les columnes de r i Vpp, per ordre, i disposades com en l'enunciat (separades per un tabulador).
#POST: retorna una llistes amb els valors r i Vpp dins.
def importa_dades():
	with open("dades.txt") as f_dades_exercici:
		ll_r = []
		ll_Vpp = []
		next(f_dades_exercici) #saltem la capçalera amb els noms de les variabl
		for linia in f_dades_exercici:
			linia = linia.split()
			r, Vpp = float(linia[0]), float(linia[1])
			ll_r += [r]
			ll_Vpp += [Vpp]
		return ll_r, ll_Vpp

#pre: llista amb valors de Vpp
#post: retorna llista amb valors ln(Vpp/Vpp0), on Vpp0 es el valor de referencia de Vpp
def calcula_valors_Y(ll_Vpp):
	ll_ln__Vpp_dividit_Vpp0 = []
	Vpp0 = ll_Vpp[0] #Vpp0 es el primer valor de la columna Vpp (1r valor de la llista)
	for i in range(len(ll_Vpp)):
		ll_ln__Vpp_dividit_Vpp0 += [math.log(ll_Vpp[i]/Vpp0)] #log es funcio ln(), en python.
	return ll_ln__Vpp_dividit_Vpp0

#pre: llista amb valors de r (distàncies)
#post: retorna llista amb valors ln(r0/r), on r0 es el valor de referencia de r
def calcula_valors_X(ll_r):
	ll_ln__r0_dividit_r = []
	r0 = ll_r[0] #r0 es el primer valor de la columna r (1r valor de la llista)
	for i in range(len(ll_r)):
		ll_ln__r0_dividit_r += [math.log(r0/ll_r[i])]
	return ll_ln__r0_dividit_r

def main_grafic():
	#CARREGUEM LES DADES DE L'ENUNCIAT
	ll_r, ll_Vpp = importa_dades()

	#CALCULEM EL VALORS DE LES Y (ln(Vpp/Vpp0) del gràfic que volem fer i, despres,
	#CALCULEM TAMBÉ EL VALORS DE LES X (ln(r0/r))
	ll_ln__Vpp_dividit_Vpp0 = calcula_valors_Y(ll_Vpp) 
	ll_ln__r0_dividit_r = calcula_valors_X(ll_r)

	#MOSTREM PER PANTALLA LES DADES QUE TENIM FINS ARA -4 COLUMNES-
	print("r     Vpp       ln(r0/r)       ln(Vpp/Vpp0")
	for i in range(len(ll_r)):
		print(ll_r[i], "   ", ll_Vpp[i], "   ", "{:.4f}    {:.4f}".format(ll_ln__r0_dividit_r[i], ll_ln__Vpp_dividit_Vpp0[i]))

	#FEM EL GRÀFIC -nuvol de punts: vermells- ENTRE ELS VALORS DE ln(r0/r)
	# -eix X- i ln(Vpp/Vpp0) -EIX Y-.
	fig, ax = plt.subplots()
	ax.plot(ll_ln__r0_dividit_r, ll_ln__Vpp_dividit_Vpp0, "ro", label = "valors empirics")
	X_regressio = np.linspace(ll_ln__r0_dividit_r[0], ll_ln__r0_dividit_r[len(ll_r) - 1], len(ll_ln__r0_dividit_r))
	
	#OBTENIM PARÀMETRES D'AJUSTAMENT DE LA RECTA DE REGRESSIO (funció de scipy: ---> https://bit.ly/2LD6wuU)
	paramtrs = scipy.stats.linregress(ll_ln__r0_dividit_r, ll_ln__Vpp_dividit_Vpp0) #a es el pendent. b és l'ordenada a l'origen
	alfa,b, r_valor = paramtrs[0], paramtrs[1], paramtrs[2]

	#CONSTRUIM LA RECTA I LA DUBUIXEM AL GRÀFIC
	Y_regressio = alfa*X_regressio + b
	ax.plot(X_regressio, Y_regressio,"g", label = "recta de regressio (minims quadrats)")
	ax.axis('equal')
	leg = ax.legend()

	#IMPRIMEIXO LA RECTA BEN FORMATEJADA I ELS SEUS. PARAMETRES, COM SI FOS UN EXCEL
	print("\nels dos paràmetres de la recta de regressió: ")
	print("  alfa (pendent):              {:.4f}".format(alfa.item()))
	print("  b    (ordenada a l'origen): {:.4f}".format(b.item()))
	print("\nla recta de regressió es: ")
	print("  y = {:.4f}x {:.4f}".format(alfa.item(),b.item()))
	print("\nel coeficient de correlacio és:")
	print("  r = {:.4f}".format(r_valor.item()))
	#AFEGIM NOM DELS EIXOS AL GRAFIC
	plt.xlabel("ln(r0/r)")
	plt.ylabel("ln(Vpp/Vpp0)")
	plt.show()

main_grafic()