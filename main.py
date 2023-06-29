import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pandas as pd
import imagem as im
import beacons as bea
import processamento as proc
import pickle
import os.path
import pygame

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

def navegar_jogo(origem, caminho):
    # Carregar a imagem como plano de fundo
    plano_fundo_original = pygame.image.load('Trabalho-grafos/planta_com_vazios.png')

    # Definir a escala desejada para a imagem
    escala = 0.2

    # Redimensionar a imagem de fundo
    largura_imagem_original, altura_imagem_original = plano_fundo_original.get_width(), plano_fundo_original.get_height()
    largura_imagem = int(largura_imagem_original * escala)
    altura_imagem = int(altura_imagem_original * escala)
    plano_fundo = pygame.transform.scale(plano_fundo_original, (largura_imagem, altura_imagem))

    # Inicializar o pygame
    pygame.init()

    # Definir as dimensões da janela do jogo
    largura_janela = largura_imagem
    altura_janela = altura_imagem

    # Criar a janela do jogo
    janela = pygame.display.set_mode((largura_janela, altura_janela))
    pygame.display.set_caption('Navegação do Usuário')

    # Definir a posição inicial do usuário
    x, y = pontos[origem]['coordenadas']
    posicao_usuario = [x*(largura_imagem/64), y*(altura_imagem/72)] # Ajustar a posição do usuário de acordo com a escala da imagem

    # Definir a posição do destino
    pOrigem = pontos[origem]['id']
    pDestino = pontos[destino]['id']
    caminho, distancia = proc.dijkstra(matrizAdjPontos, pOrigem, pDestino)
    print("Distância total: {:.2f} metros".format(distancia))

    # Definir a velocidade de movimento do usuário
    velocidade_usuario = 5

    # Loop principal do jogo
    rodando = True
    while rodando:
        # Processar eventos do pygame
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    rodando = False
                elif evento.key == pygame.K_UP:
                    posicao_usuario[1] -= velocidade_usuario
                elif evento.key == pygame.K_DOWN:
                    posicao_usuario[1] += velocidade_usuario
                elif evento.key == pygame.K_LEFT:
                    posicao_usuario[0] -= velocidade_usuario
                elif evento.key == pygame.K_RIGHT:
                    posicao_usuario[0] += velocidade_usuario
                proc.processaPosicao((float(posicao_usuario[0] / (largura_imagem / 64)), float(posicao_usuario[1] / (altura_imagem / 72))), destino, origem, caminho, pontos, listaAdjPontos, matrizAdjPontos, beacons)

        # Limpar a tela
        janela.fill((0, 0, 0))

        # Desenhar o plano de fundo na janela
        janela.blit(plano_fundo, (0, 0))

        # Desenhar a posição do usuário na imagem
        pygame.draw.circle(janela, (255, 0, 0), posicao_usuario, 5)

        # Atualizar a janela do jogo
        pygame.display.flip()

    # Encerrar o pygame
    pygame.quit()

if __name__ == "__main__":
    op = 0
    op1 = 0
    op2 = 0

    while True:
        print("Selecione a ação desejada:")
        print("1 - Plotar imagem")
        print("2 - Simular")
        print("3 - Beacons")
        print("4 - Sair")

        op = int(input())
        
        if op == 1:
            while True:
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
            origem = input("Digite o nome do ponto de origem: ")
            destino = input("Digite o nome do ponto de destino: ")
            navegar_jogo(origem, destino)
        elif op == 3:
            print(beacons)
        elif op == 4:
            break
        else:
            print("Opção inválida")
            continue