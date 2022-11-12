

import math

class Estadistica_descriptiva:
	"""classe que implementa mètodes per calcular funcions d'estadística descriptiva UNIVARIANT. a partir d'un paràmetre d'entrada: una llista de valors.
	Retorna el valor de l'operació demanada amb float i sense truncaments."""
	def __init__(self,ll):
		self.ll = ll

	def mitjana_aritmetica(self):
	  return sum(self.ll)/len(self.ll)


	def desvest(self):
	  x=Estadistica_descriptiva.mitjana_aritmetica(self) #PER QUE QUAN POSO self.ll produeix error????
	  sq=0
	  for i in range(len(self.ll)):
	    sq=sq+(self.ll[i]-x)**2
	  variansa=sq/(len(self.ll)-1)
	  desv_tip=math.sqrt(variansa)
	  return desv_tip




################################################
y = Estadistica_descriptiva([1,2,8,9])
print("\nDESCRIPTIUS")

print(y.mitjana_aritmetica())
print(y.desvest())
print("\n\n\nBIVARIANT")
################################################





class Estadistica_bivariant:
	def __init__(self,ll_x,ll_y):
		self.ll_x = ll_y
		self.ll_y = ll_y

	def covariansssa(self):
		x = Estadistica_descriptiva(self.ll_x).mitjana_aritmetica() #m'ha costat
		y = Estadistica_descriptiva(self.ll_y).mitjana_aritmetica() #m'ha costat
		sq=0
		for i in range(len(self.ll_x)):
			sq=sq+(self.ll_x[i]-x)*(self.ll_y[i]-y)
		covariansa=sq/(len(self.ll_x)-1)
		return covariansa

	def pearson(self):
		cova = Estadistica_bivariant(self.ll_x,self.ll_y).covariansssa()
		dt_x = Estadistica_descriptiva(self.ll_x).desvest()
		dt_y = Estadistica_descriptiva(self.ll_y).desvest()
		return cova / (dt_x*dt_y)




################################################
z = Estadistica_bivariant([1,2,4,5],[1,2,4,5])
print(z.covariansssa())
print(z.pearson())
################################################
