import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pandas as pd
import imagem as im
import beacons as bea
import processamento as proc
import pickle
import os.path
import numpy as np

alcance = 30

if not os.path.isfile("Trabalho-grafos/beacons.pickle"):
    matriz = im.image_to_matrix('Trabalho-grafos/planta_com_vazios.png', 72, 64)
    beacons = bea.Beacons(matriz, alcance, 3)
    beacons.calculaBeacons()
    beacons.getListaAdjacencias()
    with open("Trabalho-grafos/beacons.pickle", "wb") as f:
        pickle.dump(beacons, f)
else:
    with open("Trabalho-grafos/beacons.pickle", "rb") as f:
        beacons = pickle.load(f)

dataset = pd.read_csv('Trabalho-grafos/coords.csv')  # Extrair as informações dos beacons
pontos, listaAdjPontos, matrizAdjPontos = proc.criar_pontos(dataset)  # Extrair as informações dos pontos

def plotarImagem(opcao1, opcao2):
    # Carregar a imagem png como plano de fundo
    plano_fundo = mpimg.imread(r'Trabalho-grafos/planta_com_vazios.png')

    # Criar o plano cartesiano
    fig, ax = plt.subplots()

    # Definir a imagem JPEG como plano de fundo
    ax.imshow(plano_fundo, extent=[0, 72, 64, 0])  # Definir os limites do plano cartesiano

    for ponto, info in pontos.items():
        nome = info['nome']
        coordenadas = info['coordenadas']
        x, y = coordenadas
        ax.plot(x, y, 'ro')  # 'ro' representa o ponto vermelho
        ax.annotate(nome, (x, y), xytext=(5, 5), textcoords='offset points')

    for vertice in listaAdjPontos:
        for adj in listaAdjPontos[vertice]:
            for ponto, info in pontos.items():
                if info['id'] == vertice:
                    x1, y1 = info['coordenadas']
                if info['id'] == adj:
                    x2, y2 = info['coordenadas']
            ax.plot([x1, x2], [y1, y2], 'b-')   # 'b-' representa a linha azul

    if opcao1 == 1:
        # Plotar os beacons e suas conexões
        for i in range(len(beacons.beacons)):
            for j in range(len(beacons.beacons[0])):
                if beacons.beacons[i][j] != -1:
                    ax.plot(j, i, 'go')  # 'go' representa o beacon azul
                    ax.annotate(beacons.beacons[i][j], (j, i), xytext=(5, 5), textcoords='offset points')

                    for adj in beacons.listaAdjacencias[beacons.beacons[i][j]]:
                        for m in range(len(beacons.beacons)):
                            for n in range(len(beacons.beacons[0])):
                                if beacons.beacons[m][n] == adj:
                                    ax.plot([j, n], [i, m], 'g--')  # 'g--' representa a conexão entre beacons em linha tracejada

                    if opcao2 == 1:
                        # Adicionar o círculo em torno do beacon
                        circle = plt.Circle((j, i), radius=alcance, color='g', fill=False)
                        ax.add_artist(circle)

    plt.grid(True, color='grey', linewidth=0.5) # Adicionar a grade ao plano cartesiano

    plt.show()  # Mostrar o plano cartesiano

if __name__ == "__main__":
    op = 0
    op1 = 0
    op2 = 0


    while 1:
        print("Selecione a ação desejada:")
        print("1 - Plotar imagem")
        print("2 - Simular")
        print("3 - Sair")

        op = int(input())
        
        if op == 1:
            while 1:
                print("Com beacons ou sem beacons?")
                print("1 - Com beacons")
                print("2 - Sem beacons")
                
                op1 = int(input())

                if op1 == 1:
                    print("Com ou sem raio de alcance?")
                    print("1 - Com raio de alcance")
                    print("2 - Sem raio de alcance")
                    
                    op2 = int(input())

                    if op2 == 1:
                        break
                    elif op2 == 2:
                        break
                    else:
                        print("Opção inválida")
                        continue
                elif op1 == 2:
                    break
                else:
                    print("Opção inválida")
                    continue
            plotarImagem(op1, op2)
        elif op == 2:
            pass
        elif op == 3:
            break
        else:
            print("Opção inválida")
            continue