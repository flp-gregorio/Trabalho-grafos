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

    return pontos, listaAdjacencias

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

    caminho = []
    atual = vDestino
    while atual != -1:
        caminho.insert(0, atual)
        atual = rota[atual]

    return caminho, custo[vDestino]