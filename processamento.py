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