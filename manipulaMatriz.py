import numpy as np

def insereVertice(matriz):
    matriz = np.array(matriz)
    
    # Adiciona uma nova linha e coluna na matriz
    nova_linha = np.zeros(len(matriz))
    matriz = np.vstack([matriz, nova_linha])
    nova_coluna = np.zeros((len(matriz), 1))
    matriz = np.hstack([matriz, nova_coluna])
    matriz = np.array(matriz, 'int16')
    print(matriz)
    return matriz

def insereAresta(matrix, vi, vj):
    if matrix[vi][vj] == matrix[vj][vi]:
        matrix[vi][vj] = matrix[vi][vj] + 1
        matrix[vj][vi] = matrix[vj][vi] + 1
    else:
        matrix[vi][vj] = matrix[vi][vj] + 1
    print(matrix)

def removeAresta(matriz, vi, vj):
    matriz[vi][vj] = 0
    matriz[vj][vi] = 0
    matriz = np.array(matriz)
    print(matriz) 
    return matriz
    
def removeVertice(matriz, v):
    matriz = np.array(matriz, 'int16')
    for i in range(len(matriz)):
        for j in range(len(matriz)):
            matriz[i][v] = -1
            matriz[v][j] = -1

    print(matriz) 
    return matriz

def insereArestaLista(listaAdj, vi, vj):
    if vi in listaAdj:
        idx = 0
        while idx < len(listaAdj[vi]) and listaAdj[vi][idx] < vj:
            idx += 1
        listaAdj[vi].insert(idx, vj)
    else:
        listaAdj[vi] = [vj]
    if vj in listaAdj:
        idx = 0
        while idx < len(listaAdj[vj]) and listaAdj[vj][idx] < vi:
            idx += 1
        listaAdj[vj].insert(idx, vi)
    else:
        listaAdj[vj] = [vi]


    print(listaAdj)
    return listaAdj

def insereVerticeLista(listaAdj):
    # Obter o próximo índice disponível para o novo vértice
    v = len(listaAdj)
    
    # Adicionar o novo vértice à lista de adjacências como uma lista vazia
    listaAdj[v] = []
    
    print (listaAdj)
    return listaAdj

def removeArestaLista(listaAdj, vi, vj):
    # Verifica se vi e vj estão na lista de adjacências
    if vi in listaAdj and vj in listaAdj:
        # Remove a aresta da lista de adjacências
        if vj in listaAdj[vi]:
            listaAdj[vi].remove(vj)
        if vi in listaAdj[vj]:
            listaAdj[vj].remove(vi)
    print (listaAdj)
    return listaAdj

def removeVerticeLista(listaAdj, vi):
    # Percorre todas as listas de adjacências em busca de ocorrências de vi
    for v in listaAdj:
        # Remove todas as ocorrências de vi na lista de adjacências
        while vi in listaAdj[v]:
            listaAdj[v].remove(vi)
    # Remove a lista de adjacências de vi
    if vi in listaAdj:
        del listaAdj[vi]
    print(listaAdj)
    return listaAdj