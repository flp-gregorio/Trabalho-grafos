import numpy as np

alcance = 80 #alcance do beacon em metros

def calculaNumBeacons(matriz):
    beacons = np.zeros([len(matriz), len(matriz)])
    for i in range(len(matriz)):
        for j in range(len(matriz)):
            if matriz[i][j] == -1:  #não faz parte da planta
                continue 
            while matriz[i][j] < 3: #não tem cobertura de 3 beacons
                adicionaBeacon(matriz, i, j, beacons)

def adicionaBeacon(matriz, i, j, beacons):
    #a ideia do código é achar a posição do beacon que gerará a maior cobertura possível
    
    cobertura = 0

    for x in range(-alcance, alcance):
        if i+x < 0 or i+x >= len(matriz):   #verifica se a posição está dentro da matriz
            continue
        else:
            if matriz[i+x][j] == -1:
                continue
            elif beacons[i+x][j] == 0:    #verifica se já existe um beacon na posição
                if calculaCobertura(matriz, i+x, j, beacons) > cobertura:   #se vai aumentar a maior cobertura encontranda anteriormente
                    cobertura = calculaCobertura(matriz, i+x, j, beacons)
                    posX = i+x
                    posY = j

def calculaCobertura(matriz, i, j, beacons):
    pass