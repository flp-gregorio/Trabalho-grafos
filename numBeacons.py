import numpy as np

alcance = 80 #alcance do beacon em metros
coberturaMin = 3 #cobertura mínima de beacons necessária em um ponto
cont = 0 #contador de beacons

def calculaNumBeacons(matriz):
    beacons = np.zeros([len(matriz), len(matriz)])
    for i in range(len(matriz)):
        for j in range(len(matriz)):
            if matriz[i][j] == -1:  #não faz parte da planta
                continue 
            while matriz[i][j] <= coberturaMin: #não tem cobertura de 3 beacons
                adicionaBeacon(matriz, i, j, beacons)

def adicionaBeacon(matriz, i, j, beacons):
    #a ideia do código é achar a posição do beacon que gerará a maior cobertura possível
    
    cobertura = 0

    for x in range(-alcance, alcance+1):    #calcula a melhor cobertura para posições do beacon no eixo x
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

    for y in range(-alcance, alcance+1):    #calcula a melhor cobertura para posições do beacon no eixo y
        if j+y < 0 or j+y >= len(matriz[0]):
            continue
        else:
            if matriz[i][j+y] == -1:
                continue
            elif beacons[i][j+y] == 0:
                if calculaCobertura(matriz, i, j+y, beacons) > cobertura:
                    cobertura = calculaCobertura(matriz, i, j+y, beacons)
                    posX = i
                    posY = j+y

    beacons[posX][posY] = cont
    cont += 1

def calculaCobertura(matriz, i, j, beacons):
    cobertura = 0
    
    for x in range(-alcance, alcance+1):
        for y in range(-alcance, alcance+1):
            if x**2 + y**2 <= alcance**2:  # verifica se a posição (x, y) está dentro do alcance circular
                if i+x < 0 or i+x >= len(matriz) or j+y < 0 or j+y >= len(matriz[0]):  # verifica se a posição está dentro da matriz
                    continue
                elif matriz[i+x][j+y] != -1 and beacons[i+x][j+y] == 0:  # verifica se a posição não é um obstáculo e não possui um beacon
                    cobertura += coberturaMin - matriz[i+x][j+y]  # adiciona a cobertura do beacon na posição (x, y) com prioridade para os pontos com menor cobertura
    
    return cobertura