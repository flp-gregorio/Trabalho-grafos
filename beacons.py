import math
import numpy as np

class Beacons:
    def __init__(self, matriz, alcance, coberturaMin):
        self._matriz = matriz
        self._alcance = alcance
        self._coberturaMin = coberturaMin

        self._beacons = [[-1] * len(matriz[0]) for _ in range(len(matriz))]
        self._idBeacons = -1

        self._matrizAdjacencias = None
        self._listaAdjacencias = None

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

    @property
    def matrizAdjacencias(self):
        return self._matrizAdjacencias
    
    @matrizAdjacencias.setter
    def matrizAdjacencias(self, matrizAdjacencias):
        self._matrizAdjacencias = matrizAdjacencias

    @property
    def listaAdjacencias(self):
        return self._listaAdjacencias
    
    @listaAdjacencias.setter
    def listaAdjacencias(self, listaAdjacencias):
        self._listaAdjacencias = listaAdjacencias

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
    
    def matrizAdjacenciasBeacons(self):
        #cria uma matriz de adjacências dos beacons analisando a matriz de beacons e encontrando os beacons adjacentes

        self._matrizAdjacencias = [[0] * (self._idBeacons+1) for _ in range(self._idBeacons+1)]

        for i in range(len(self._beacons)):
            for j in range(len(self._beacons[0])):
                if self._beacons[i][j] == -1:
                    continue
                for x in range(-self._alcance, self._alcance+1):
                    for y in range(-self._alcance, self._alcance+1):
                        if x**2 + y**2 <= self._alcance**2:
                            if i+x < 0 or i+x >= len(self._beacons) or j+y < 0 or j+y >= len(self._beacons[0]):
                                continue
                            elif self._beacons[i+x][j+y] != -1 and self._beacons[i+x][j+y] != self._beacons[i][j]:
                                self._matrizAdjacencias[self._beacons[i][j]][self._beacons[i+x][j+y]] = 1

        return np.array(self._matrizAdjacencias)
    
    def listaAdjacenciasBeacons(self):
        #cria uma lista de adjacências dos beacons analisando a matriz de beacons e encontrando os beacons adjacentes

        self._listaAdjacencias = {}

        if self._matrizAdjacencias == None:
            self.matrizAdjacenciasBeacons() #cria a matriz de adjacências dos beacons

        #transforma a matriz de adjacências em uma lista de adjacências
        for i in range(len(self._matrizAdjacencias)):
            self._listaAdjacencias[i] = []
            for j in range(len(self._matrizAdjacencias)):
                num = self._matrizAdjacencias[i][j]
                while num>0:   #se houverem mais arestas, o vértice será repetido
                    self._listaAdjacencias[i].append(j)
                    num -= 1

        return self._listaAdjacencias

    def getMatrizAdjacencias(self):
        if self._matrizAdjacencias == None:
            return str(np.array(self.matrizAdjacenciasBeacons()))
        else:
            return str(np.array(self._matrizAdjacencias))

    def getListaAdjacencias(self):
        if self._listaAdjacencias == None:
            return str(self.listaAdjacenciasBeacons())
        else:
            return str(self._listaAdjacencias)
        
    def getBeacons(self):
        if self._idBeacons == -1:
            return str(np.array(self.calculaBeacons()))
        else:
            return str(np.array(self._beacons))
    
    def getMatriz(self):
        return str(np.array(self._matriz))
    
    def getNumBeacons(self):
        return str(self._idBeacons + 1)
    
    def __str__(self):
        ret = ""

        ret += "Cobertura mínima: " + str(self.coberturaMin) + "\n\n"
        ret += "Alcance: " + str(self.alcance) + "\n\n"
        ret += "Matriz de cobertura:\n"
        ret += self.getMatriz() + "\n\n"
        ret += "Matriz de beacons:\n"
        ret += self.getBeacons() + "\n\n"
        ret += "Número de beacons: " + self.getNumBeacons() + "\n\n"
        ret += "Matriz de adjacências:\n"
        ret += self.getMatrizAdjacencias() + "\n\n"
        ret += "Lista de adjacências:\n"
        ret += self.getListaAdjacencias() + "\n"

        return ret