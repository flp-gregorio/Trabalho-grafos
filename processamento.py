import math

def criar_pontos(dataset):
    pontos = {}
    listaAdjacencias = {}

    for _, row in dataset.iterrows():
        id = _
        nome = row['nome']
        x = row['x']
        y = row['y']
        adjacencias = [int(adj) for adj in row['adjacencias'].split(',')] if row['adjacencias'] else []

        listaAdjacencias[id] = adjacencias

        pontos[nome] = {'nome': nome, 'coordenadas': (x, y), 'adjacencias': adjacencias, 'id': id}

    matrizAdjacencias = [[-1 for _ in range(len(listaAdjacencias))] for _ in range(len(listaAdjacencias))]

    for vertice in listaAdjacencias:
        for adj in listaAdjacencias[vertice]:
            for ponto, info in pontos.items():
                if info['id'] == vertice:
                    x1, y1 = info['coordenadas']
                if info['id'] == adj:
                    x2, y2 = info['coordenadas']
            matrizAdjacencias[vertice][adj] = distancia((x1, y1), (x2, y2))

    return pontos, listaAdjacencias, matrizAdjacencias

def distancia(ponto1, ponto2):
    x1, y1 = ponto1
    x2, y2 = ponto2

    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

import math

def dijkstra(matriz, vOrigem, vDestino):
    numVertices = len(matriz)
    custo = [math.inf] * numVertices
    rota = [-1] * numVertices
    custo[vOrigem] = 0

    verAbertos = set(range(numVertices))
    verFechados = set()

    while verAbertos:
        v = min(verAbertos, key=lambda x: custo[x])
        verAbertos.remove(v)
        verFechados.add(v)

        if v == vDestino:
            break

        for j in range(numVertices):
            if j not in verFechados and matriz[v][j] != -1:
                aresta = matriz[v][j]
                dist = custo[v] + aresta
                if dist < custo[j]:
                    custo[j] = dist
                    rota[j] = v

        for j in range(numVertices):
            if j not in verFechados and matriz[j][v] != -1:
                aresta = matriz[j][v]
                dist = custo[v] + aresta
                if dist < custo[j]:
                    custo[j] = dist
                    rota[j] = v

    caminho = []
    atual = vDestino
    while atual != -1:
        caminho.insert(0, atual)
        atual = rota[atual]

    return caminho, custo[vDestino]

def print_matrix(matrix):
    for row in matrix:
        print(' '.join('{:2d}'.format(pixel) for pixel in row))

def processaPosicao(posicao_usuario, destino, origem, caminho, pontos, listaAdjPontos, matrizAdjPontos):
    pass