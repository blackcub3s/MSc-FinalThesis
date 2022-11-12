import numpy as np

# defineixo limits d integracio i array de valors per a x i per a y.
# aixi com la precisio, o nombre de "rectangles amb triangle a dalt" - 1
# que hi haura per aproximar la integral definida entre els dos limits.
# prova: integral definida de y = x**2 entre els valors
# 2 i 5. El resultat numeric es 39 just. l aproximacio hauria de ser
# similar i este clavat.


li = 2
ls = 5
#li=0
#ls=2*np.pi
nre_rectanglets_menys_un = 5000
x = np.linspace(li,ls,nre_rectanglets_menys_un)
#y=np.sin(x)  #DONARA ZERO, COMBINADA AMB ELS LI I LS DE LES LINIES 13 I 14 (I MUTEJANT ELS DE LA LINIA 11 I 12)
y = x**2


def integral_definida():
    area_acumulativa=0
    for i in range(len(x)-1):
        mini_rect = (x[i+1]-x[i])*(y[i+1]+(y[i]-y[i+1])/2)
        area_acumulativa = area_acumulativa + mini_rect
    return area_acumulativa


print(integral_definida())

