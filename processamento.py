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

import math

def processaPosicao(posicao_usuario, destino, origem, caminho, pontos, listaAdjPontos, matrizAdjPontos, beacons):
    #Encontrar a posição do usuário no grafo baseado nos beacons próximos
    posicaoCalc = encontrarPosicaoUsuario(encontrarBeaconsProximos(posicao_usuario, beacons), pontos, listaAdjPontos, matrizAdjPontos, posicao_usuario)

    print('Posição calculada: {}'.format(posicaoCalc))

def encontrarBeaconsProximos(posicao_usuario, beacons):
    i, j = posicao_usuario
    beaconsEncontrados = []

    for x in range(-beacons.alcance, beacons.alcance + 1):
        for y in range(-beacons.alcance, beacons.alcance + 1):
            if x**2 + y**2 <= beacons.alcance**2:  # verifica se a posição (x, y) está dentro do alcance circular
                if i + x < 0 or i + x >= len(beacons.beacons) or j + y < 0 or j + y >= len(beacons.beacons[0]):  # verifica se a posição está dentro da matriz de beacons
                    continue
                elif beacons.beacons[x][y] != -1:  # verifica se há um beacon na posição (x, y)
                    beaconsEncontrados.append((x, y))
                    if len(beaconsEncontrados) == 3:    #encerra a busca quando encontrar 3 beacons
                        print('Beacons encontrados: {}'.format(beaconsEncontrados))
                        return beaconsEncontrados

def encontrarPosicaoUsuario(beacons_proximos, pontos, listaAdjPontos, matrizAdjPontos, posicao_usuario):
    # Encontrar a posição do usuário no grafo baseado nos beacons próximos
    distancias = []

    for i in range(len(beacons_proximos)):
        distancias.append(distancia(posicao_usuario, beacons_proximos[i]))

    return trilateracao(distancias[0], distancias[1], distancias[2], beacons_proximos[0], beacons_proximos[1], beacons_proximos[2])

def trilateracao(distanciaA, distanciaB, distanciaC, pontoA, pontoB, pontoC):
    # Cálculo das diferenças de coordenadas
    diff_AB = (pontoB[0] - pontoA[0], pontoB[1] - pontoA[1])
    diff_AC = (pontoC[0] - pontoA[0], pontoC[1] - pontoA[1])

    # Cálculo das distâncias entre os pontos de referência
    d_AB = math.sqrt(diff_AB[0] ** 2 + diff_AB[1] ** 2)
    d_AC = math.sqrt(diff_AC[0] ** 2 + diff_AC[1] ** 2)

    # Cálculo das coordenadas de P
    t = (distanciaA ** 2 - distanciaB ** 2 + d_AB ** 2) / (2 * d_AB)
    x = (distanciaA ** 2 - distanciaC ** 2 + d_AC ** 2 + 2 * diff_AC[0] * t) / (2 * diff_AC[0])
    y = ((distanciaA ** 2 - distanciaC ** 2 + d_AC ** 2 + 2 * diff_AC[0] * t) ** 2 - x ** 2) ** 0.5

    # Coordenadas de P
    pontoP = (pontoA[0] + x, pontoA[1] + y)

    return pontoP