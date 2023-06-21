import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pandas as pd
import entradaSaida as es

def dijkstra(matriz, vOrigem, vDestino):
    n = len(matriz)
    infinito = float('inf')
    custo = [infinito] * n
    custo[vOrigem] = 0
    rota = [-1] * n

    F = set()
    A = set(range(n))
    N = set()

    while A:
        v = min(A, key=lambda u: custo[u])
        if v == vDestino:
            break
        A.remove(v)
        F.add(v)

        for u in range(n):
            if u in A and matriz[v][u] != -1:
                wvu = matriz[v][u]
                novaDistancia = custo[v] + wvu
                if novaDistancia < custo[u]:
                    custo[u] = novaDistancia
                    rota[u] = v
                    N.add(u)

        A.update(N)
        N.clear()

    caminho = []
    vertice = vDestino
    while vertice != -1:
        caminho.insert(0, vertice)
        vertice = rota[vertice]

    print(caminho, custo[vDestino])



def criar_beacons(dataset):
    beacons = {}

    for _, row in dataset.iterrows():
        id_beacon = row['id']
        x = row['x']
        y = row['y']
        adjacencias = [int(adj) for adj in row['adjacencias'].split(',')] if row['adjacencias'] else []

        beacons[id_beacon] = {'nome': id_beacon, 'coordenadas': (x, y), 'adjacencias': adjacencias}

    return beacons

import numpy as np

def listaParaMatriz(adjacencias):
    vertices = sorted(adjacencias.keys())
    n = len(vertices)
    mapa_vertices = {v: i for i, v in enumerate(vertices)}
    matriz = np.full((n, n), -1)

    for v, info in adjacencias.items():
        i = mapa_vertices[v]
        adj = info['adjacencias']
        for u in adj:
            j = mapa_vertices.get(str(u))
            if j is not None:
                matriz[i][j] = 1  # Definir o peso da aresta como 1 (ou o valor desejado)

    return matriz




dataset = pd.read_csv('./Instancias/coords.csv') # Extrair as informações dos beacons




# Carregar a imagem JPEG como plano de fundo
plano_fundo = mpimg.imread(r'C:\Users\Felip\Documents\Cenário 3 - Dados\img8.jpg')

# Criar o plano cartesiano
fig, ax = plt.subplots()

# Definir a imagem JPEG como plano de fundo
ax.imshow(plano_fundo, extent=[0, 100, 0, 100])  # Definir os limites do plano cartesiano

# Plotar os elementos no plano cartesiano
beacons = criar_beacons(dataset)
dijkstra(listaParaMatriz(beacons), 1, 19)
print(beacons.keys())

# Plotar os beacons no plano cartesiano
for beacon, info in beacons.items():
    nome = info['nome']
    coordenadas = info['coordenadas']
    x, y = coordenadas
    ax.plot(x, y, 'ro')  # 'ro' representa o ponto vermelho
    ax.annotate(nome, (x, y), xytext=(5, 5), textcoords='offset points')

# Configurar as legendas
ax.legend()

# Mostrar o plano cartesiano com o plano de fundo
plt.show()