import numpy as np
from scipy.spatial import Voronoi, voronoi_plot_2d
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

def run_voronoi(beacons):
    points = [beacon['coordenadas'] for beacon in beacons.values()]  # Extract the coordinates of the vertices
    vor = Voronoi(points)  # Perform Voronoi tessellation

    voronoi_cells = {}
    for ridge_points, ridge_vertices in vor.ridge_dict.items():
        if -1 in ridge_vertices:  # Skip infinite ridges
            continue
        
        v1, v2 = ridge_points
        vertex1 = points[v1]
        vertex2 = points[v2]
        
        # Calculate the midpoint between the two vertices
        midpoint = ((vertex1[0] + vertex2[0]) / 2, (vertex1[1] + vertex2[1]) / 2)
        
        # Calculate the perpendicular bisector slope
        if vertex1[0] == vertex2[0]:  # Vertical line
            slope = None
        else:
            slope = (vertex2[1] - vertex1[1]) / (vertex2[0] - vertex1[0])
            slope = -1 / slope if slope != 0 else None
        
        # Extend the line segment until it intersects with the bounding box
        if slope is None:
            x = [midpoint[0], midpoint[0]]
            y = [vor.min_bound[1], vor.max_bound[1]]
        else:
            b = midpoint[1] - slope * midpoint[0]
            x = [vor.min_bound[0], vor.max_bound[0]]
            y = [slope * xi + b for xi in x]
        
        # Store the Voronoi edge as a line segment
        edge = [(x[0], y[0]), (x[1], y[1])]
        
        # Find the corresponding vertex ID for the Voronoi edge
        vertex_id = None
        for key, value in beacons.items():
            if value['coordenadas'] == vertex1 or value['coordenadas'] == vertex2:
                vertex_id = key
                break
        
        # Add the edge to the corresponding Voronoi cell
        if vertex_id:
            if vertex_id not in voronoi_cells:
                voronoi_cells[vertex_id] = []
            voronoi_cells[vertex_id].append(edge)

    return voronoi_cells

dataset = pd.read_csv('./coords.csv') # Extrair as informações dos beacons

# Carregar a imagem JPEG como plano de fundo
plano_fundo = mpimg.imread(r'planta.jpeg')

# Criar o plano cartesiano
fig, ax = plt.subplots()

# Definir a imagem JPEG como plano de fundo
ax.imshow(plano_fundo, extent=[0, 100, 0, 100])  # Definir os limites do plano cartesiano

# Plotar os elementos no plano cartesiano
beacons = criar_beacons(dataset)
voronoi_cells = run_voronoi(beacons)
dijkstra(listaParaMatriz(beacons), 1, 19)

# Plotar os beacons no plano cartesiano
for beacon, info in beacons.items():
    nome = info['nome']
    coordenadas = info['coordenadas']
    x, y = coordenadas
    ax.plot(x, y, 'ro')  # 'ro' representa o ponto vermelho
    ax.annotate(nome, (x, y), xytext=(5, 5), textcoords='offset points')

# Configurar as legendas
#ax.legend()

plt.grid(True, color='grey', linewidth=0.5)  # Adicionar a grade ao plano cartesiano

# Mostrar o plano cartesiano com o plano de fundo
plt.show()

# Visualize the Voronoi diagram
fig, ax2 = plt.subplots()
voronoi_plot_2d(Voronoi([beacon['coordenadas'] for beacon in beacons.values()]), ax2=ax2)
for cell in voronoi_cells.values():
    for edge in cell:
        ax2.plot(*zip(*edge), color='red')  # Plot Voronoi edges
plt.show()