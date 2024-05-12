# Readme para o Projeto de Navegação Indoor para Deficientes Visuais

## Visão Geral

Este projeto desenvolve um sistema de navegação indoor voltado para auxiliar pessoas com deficiência visual a se locomoverem de forma autônoma e segura dentro de ambientes fechados, como universidades, hospitais e shoppings. O sistema utiliza beacons Bluetooth Low Energy (BLE) para determinar a localização do usuário e um aplicativo móvel para guiar o usuário até seu destino por meio de instruções de voz.

## Estrutura do Projeto

O código do projeto está organizado nos seguintes módulos principais:

1. **main.py** - Arquivo principal que executa a aplicação, tratando da inicialização e interação com o usuário.
2. **imagem.py** - Contém funções para converter imagens de plantas baixas em matrizes utilizáveis pelo sistema.
3. **processamento.py** - Responsável pelo processamento dos dados de navegação, incluindo a criação de pontos de navegação e a execução do algoritmo de Dijkstra para encontrar o menor caminho.
4. **beacons.py** - Define a classe `Beacons` e métodos associados para o cálculo de posicionamento e cobertura dos beacons.
5. **planta_com_vazios.png** - Imagem da planta baixa utilizada para a navegação.
6. **coords.csv** - Dataset com informações sobre os pontos de interesse e suas adjacências dentro da planta baixa.

## Funcionalidades

### Navegação Baseada em Beacons

Utiliza beacons BLE distribuídos estrategicamente pela planta do edifício para determinar a posição do usuário e fornecer direções até o destino desejado.

### Simulação Visual

Um sistema de simulação visual no `pygame` que mostra a trajetória do usuário pela planta baixa, ajudando no desenvolvimento e testes do sistema de navegação.

### Análise de Robustez

Inclui uma análise da fragilidade da rede de beacons, identificando pontos críticos cuja falha pode comprometer a navegação.

## Requisitos

- Python 3.8+
- Bibliotecas Python: `matplotlib`, `pandas`, `PIL`, `pygame`, `numpy`

## Setup e Execução

1. Instale Python e as dependências necessárias:
   ```bash
   pip install matplotlib pandas pillow pygame numpy
   ```

2. Clone o repositório ou baixe os arquivos do projeto.

3. Execute o arquivo `main.py`:
   ```bash
   python main.py
   ```

4. Siga as instruções no menu interativo para visualizar a planta, simular a navegação ou visualizar informações dos beacons.

## Uso

Ao executar o programa, você terá as seguintes opções:

1. **Plotar imagem**: Exibe a planta baixa com ou sem beacons e suas conexões, com opções para mostrar ou não o raio de alcance.
2. **Simular**: Permite ao usuário inserir um ponto de origem e destino para simular a navegação no jogo.
3. **Beacons**: Exibe informações detalhadas sobre os beacons, incluindo número, distribuição e matrizes de adjacência.
4. **Sair**: Encerra a aplicação.

## Contribuições

Contribuições são bem-vindas. Para contribuir, por favor, abra um pull request com suas sugestões ou correções.

## Autores

- Felipe Alves Gregorio
- Leandro Rocha Liberato Gonçalves
