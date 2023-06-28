import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pandas as pd
import imagem as im
import beacons as bea
import processamento as proc
import pickle
import os.path

if not os.path.isfile("beacons.pickle"):
    matriz = im.image_to_matrix('Trabalho-grafos/planta_com_vazios.png', 72, 64)
    beacons = bea.Beacons(matriz, 40, 3)
    beacons.calculaBeacons()
    with open("Trabalho-grafos/beacons.pickle", "wb") as f:
        pickle.dump(beacons, f)
else:
    with open("Trabalho-grafos/beacons.pickle", "rb") as f:
        beacons = pickle.load(f)

dataset = pd.read_csv('Trabalho-grafos/coords.csv')  # Extrair as informações dos beacons

# Carregar a imagem png como plano de fundo
plano_fundo = mpimg.imread(r'Trabalho-grafos/planta_com_vazios.png')

# Criar o plano cartesiano
fig, ax = plt.subplots()

# Definir a imagem JPEG como plano de fundo
ax.imshow(plano_fundo, extent=[0, 72, 64, 0])  # Definir os limites do plano cartesiano

pontos = proc.criar_pontos(dataset)  # Extrair as informações dos pontos

for ponto, info in pontos.items():
    nome = info['nome']
    coordenadas = info['coordenadas']
    x, y = coordenadas
    ax.plot(x, y, 'ro')  # 'ro' representa o ponto vermelho
    ax.annotate(nome, (x, y), xytext=(5, 5), textcoords='offset points')

plt.grid(True, color='grey', linewidth=0.5)  # Adicionar a grade ao plano cartesiano

plt.show()  # Mostrar o plano cartesiano