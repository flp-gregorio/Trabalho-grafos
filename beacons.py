import math
import numpy as np

class Beacons:
    def __init__(self, matriz, alcance, coberturaMin):
        self.matriz = matriz
        self.alcance = alcance
        self.coberturaMin = coberturaMin

        self.beacons = [[-1] * len(matriz[0]) for i in range(len(matriz))]
        self.numBeacons = -1

    @property
    def matriz(self):
        return self.matriz
    
    @matriz.setter
    def matriz(self, matriz):
        if len(matriz) < 1 or len(matriz[0]) < 1:
            raise ValueError("A matriz deve ter pelo menos 1 linha e 1 coluna")
        self.matriz = matriz

    @property
    def alcance(self):
        return self.alcance
    
    @alcance.setter
    def alcance(self, alcance):
        if alcance < 1:
            raise ValueError("O alcance deve ser maior ou igual a 1")
        self.alcance = alcance

    @property
    def coberturaMin(self):
        return self.coberturaMin
    
    @coberturaMin.setter
    def coberturaMin(self, coberturaMin):
        if coberturaMin < 1:
            raise ValueError("A cobertura mínima deve ser maior ou igual a 1")
        self.coberturaMin = coberturaMin

    @property
    def beacons(self):
        return self.beacons
    
    @beacons.setter
    def beacons(self, beacons):
        if len(beacons) < 1 or len(beacons[0]) < 1:
            raise ValueError("A matriz de beacons deve ter pelo menos 1 linha e 1 coluna")
        self.beacons = beacons

    @property
    def numBeacons(self):
        return self.numBeacons
    
    @numBeacons.setter
    def numBeacons(self, numBeacons):
        if numBeacons < -1:
            raise ValueError("O número de beacons deve ser maior ou igual a -1")
        self.numBeacons = numBeacons

    def calculaBeacons(self):
        for i in range(len(self.matriz)):
            for j in range(len(self.matriz)):
                if self.matriz[i][j] == -1:  #não faz parte da planta
                    continue 
                while self.matriz[i][j] < self.coberturaMin: #não tem cobertura de 3 beacons
                    self.adicionaBeacon(i, j)

        return self.beacons

    def adicionaBeacon(self, i, j):
        #a ideia do código é achar a posição do beacon que gerará a maior cobertura possível
        
        cobertura = -math.inf

        #calcula a melhor posição para o beacon dentro do raio do ponto analisado
        for x in range(-self.alcance, self.alcance+1):
            for y in range(-self.alcance, self.alcance+1):
                if x**2 + y**2 <= self.alcance**2:  # verifica se a posição (x, y) está dentro do alcance circular
                    if i+x < 0 or i+x >= len(self.matriz) or j+y < 0 or j+y >= len(self.matriz[0]):  # verifica se a posição está dentro da matriz
                        continue
                    elif self.matriz[i+x][j+y] != -1 and self.beacons[i+x][j+y] == -1: # verifica se a posição não é um obstáculo e não possui um beacon
                        coberturaCalculada = self.calculaCobertura(i+x, j+y) #calcula a cobertura da posição (x, y)
                        if coberturaCalculada > cobertura: #verifica se a cobertura é maior que a anterior
                            cobertura = coberturaCalculada
                            posX = i+x
                            posY = j+y

        self.numBeacons += 1
        self.beacons[posX][posY] = self.numBeacons

        #atualiza a cobertura dos pontos ao redor do beacon adicionado
        for x in range(-self.alcance, self.alcance+1):
            for y in range(-self.alcance, self.alcance+1):
                if x**2 + y**2 <= self.alcance**2:
                    if posX+x < 0 or posX+x >= len(self.matriz) or posY+y < 0 or posY+y >= len(self.matriz[0]):
                        continue
                    elif self.matriz[posX+x][posY+y] != -1:
                        self.matriz[posX+x][posY+y] += 1

    def calculaCobertura(self, i, j):
        cobertura = 0
        
        for x in range(-self.alcance, self.alcance+1):
            for y in range(-self.alcance, self.alcance+1):
                if x**2 + y**2 <= self.alcance**2:  # verifica se a posição (x, y) está dentro do alcance circular
                    if i+x < 0 or i+x >= len(self.matriz) or j+y < 0 or j+y >= len(self.matriz[0]):  # verifica se a posição está dentro da matriz
                        continue
                    elif self.matriz[i+x][j+y] != -1 and self.beacons[i+x][j+y] == -1:  # verifica se a posição não é um obstáculo e não possui um beacon
                        cobertura += self.coberturaMin - self.matriz[i+x][j+y]  # adiciona a cobertura do beacon na posição (x, y) com prioridade para os pontos com menor cobertura

        return cobertura

    def getBeacons(self):
        return str(np.array(self.beacons))
    
    def getMatriz(self):
        return str(np.array(self.matriz))