alcance = 80 #alcance do beacon em metros
coberturaMin = 3 #cobertura mínima de beacons necessária em um ponto
cont = [1] #contador de beacons
cont[0] = 0

def posicionaBeacons(matriz, alcance, coberturaMin):
    cont = [1] #contador de beacons
    cont[0] = 0

    def calculaBeacons(matriz):
        beacons = [[-1] * len(matriz[0]) for i in range(len(matriz))]  # matriz de beacons, -1 = não possui beacon, 0, 1, 2, 3, ... = id do beacon
        
        for i in range(len(matriz)):
            for j in range(len(matriz)):
                if matriz[i][j] == -1:  #não faz parte da planta
                    continue 
                while matriz[i][j] <= coberturaMin: #não tem cobertura de 3 beacons
                    adicionaBeacon(matriz, i, j, beacons)

        return beacons

    def adicionaBeacon(matriz, i, j, beacons):
        #a ideia do código é achar a posição do beacon que gerará a maior cobertura possível
        
        cobertura = 0

        #calcula a melhor posição para o beacon dentro do raio do ponto analisado
        for x in range(-alcance, alcance+1):
            for y in range(-alcance, alcance+1):
                if x**2 + y**2 <= alcance**2:  # verifica se a posição (x, y) está dentro do alcance circular
                    if i+x < 0 or i+x >= len(matriz) or j+y < 0 or j+y >= len(matriz[0]):  # verifica se a posição está dentro da matriz
                        continue
                    elif matriz[i+x][j+y] != -1 and beacons[i+x][j+y] == 0: # verifica se a posição não é um obstáculo e não possui um beacon
                        if calculaCobertura(matriz, i+x, j+y, beacons) > cobertura: #verifica se a cobertura é maior que a anterior
                            cobertura = calculaCobertura(matriz, i+x, j+y, beacons)
                            posX = i+x
                            posY = j+y

        beacons[posX][posY] = cont[0]
        cont[0] += 1

        #atualiza a cobertura dos pontos ao redor do beacon adicionado
        for x in range(-alcance, alcance+1):
            for y in range(-alcance, alcance+1):
                if x**2 + y**2 <= alcance**2:
                    if posX+x < 0 or posX+x >= len(matriz) or posY+y < 0 or posY+y >= len(matriz[0]):
                        continue
                    elif matriz[posX+x][posY+y] != -1 and beacons[posX+x][posY+y] == 0:
                        matriz[posX+x][posY+y] += 1

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
    
    return calculaBeacons(matriz)
    
posicionaBeacons(matriz, 80, 3)