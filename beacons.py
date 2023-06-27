import math
import numpy as np

class Beacons:
    def __init__(self, matriz, alcance, coberturaMin):
        self._matriz = matriz
        self._alcance = alcance
        self._coberturaMin = coberturaMin

        self._beacons = [[-1] * len(matriz[0]) for _ in range(len(matriz))]
        self._idBeacons = -1

    @property
    def matriz(self):
        return self._matriz
    
    @matriz.setter
    def matriz(self, matriz):
        if len(matriz) < 1 or len(matriz[0]) < 1:
            raise ValueError("A matriz deve ter pelo menos 1 linha e 1 coluna")
        self._matriz = matriz

    @property
    def alcance(self):
        return self._alcance
    
    @alcance.setter
    def alcance(self, alcance):
        if alcance < 1:
            raise ValueError("O alcance deve ser maior ou igual a 1")
        self._alcance = alcance

    @property
    def coberturaMin(self):
        return self._coberturaMin
    
    @coberturaMin.setter
    def coberturaMin(self, coberturaMin):
        if coberturaMin < 1:
            raise ValueError("A cobertura mínima deve ser maior ou igual a 1")
        self._coberturaMin = coberturaMin

    @property
    def beacons(self):
        return self._beacons
    
    @beacons.setter
    def beacons(self, beacons):
        if len(beacons) < 1 or len(beacons[0]) < 1:
            raise ValueError("A matriz de beacons deve ter pelo menos 1 linha e 1 coluna")
        self._beacons = beacons

    @property
    def idBeacons(self):
        return self._idBeacons
    
    @idBeacons.setter
    def idBeacons(self, idBeacons):
        if idBeacons < -1:
            raise ValueError("O número de beacons deve ser maior ou igual a -1")
        self._idBeacons = idBeacons

    def calculaBeacons(self):
        for i in range(len(self._matriz)):
            for j in range(len(self._matriz[0])):
                if self._matriz[i][j] == -1:  #não faz parte da planta
                    continue 
                while self._matriz[i][j] < self._coberturaMin: #não tem cobertura de 3 beacons
                    self.adicionaBeacon(i, j)

        return self._beacons

    def adicionaBeacon(self, i, j):
        #a ideia do código é achar a posição do beacon que gerará a maior cobertura possível
        
        cobertura = -math.inf

        #calcula a melhor posição para o beacon dentro do raio do ponto analisado
        for x in range(-self._alcance, self._alcance+1):
            for y in range(-self._alcance, self._alcance+1):
                if x**2 + y**2 <= self._alcance**2:  # verifica se a posição (x, y) está dentro do alcance circular
                    if i+x < 0 or i+x >= len(self._matriz) or j+y < 0 or j+y >= len(self._matriz[0]):  # verifica se a posição está dentro da matriz
                        continue
                    elif self._matriz[i+x][j+y] != -1 and self._beacons[i+x][j+y] == -1: # verifica se a posição não é um obstáculo e não possui um beacon
                        coberturaCalculada = self.calculaCobertura(i+x, j+y) #calcula a cobertura da posição (x, y)
                        if coberturaCalculada > cobertura: #verifica se a cobertura é maior que a anterior
                            cobertura = coberturaCalculada
                            posX = i+x
                            posY = j+y

        self._idBeacons += 1
        self._beacons[posX][posY] = self._idBeacons

        #atualiza a cobertura dos pontos ao redor do beacon adicionado
        for x in range(-self._alcance, self._alcance+1):
            for y in range(-self._alcance, self._alcance+1):
                if x**2 + y**2 <= self._alcance**2:
                    if posX+x < 0 or posX+x >= len(self._matriz) or posY+y < 0 or posY+y >= len(self._matriz[0]):
                        continue
                    elif self._matriz[posX+x][posY+y] != -1:
                        self._matriz[posX+x][posY+y] += 1

    def calculaCobertura(self, i, j):
        cobertura = 0
        
        for x in range(-self._alcance, self._alcance+1):
            for y in range(-self._alcance, self._alcance+1):
                if x**2 + y**2 <= self._alcance**2:  # verifica se a posição (x, y) está dentro do alcance circular
                    if i+x < 0 or i+x >= len(self._matriz) or j+y < 0 or j+y >= len(self._matriz[0]):  # verifica se a posição está dentro da matriz
                        continue
                    elif self._matriz[i+x][j+y] != -1 and self._beacons[i+x][j+y] == -1:  # verifica se a posição não é um obstáculo e não possui um beacon
                        cobertura += self._coberturaMin - self._matriz[i+x][j+y]  # adiciona a cobertura do beacon na posição (x, y) com prioridade para os pontos com menor cobertura

        return cobertura

    def getBeacons(self):
        return np.array(self._beacons)
    
    def getMatriz(self):
        return np.array(self._matriz)
    
    def getNumBeacons(self):
        return self._idBeacons + 1


if __name__ == "__main__":
    x = 80  # número de linhas
    y = 70  # número de colunas
    num_minus_ones = 2240  # quantidade de elementos -1

    matriz = [[0] * y for _ in range(x)]

    import random

    for _ in range(num_minus_ones):
        i = random.randint(0, x - 1)
        j = random.randint(0, y - 1)
        matriz[i][j] = -1

    beacon = Beacons(matriz, 80, 3)

    beacon.calculaBeacons()
    print(beacon.getBeacons())
    print(beacon.getMatriz())
    print(beacon.getNumBeacons())