def criar_pontos(dataset):
    pontos = {}

    for _, row in dataset.iterrows():
        id_ponto = row['id']
        x = row['x']
        y = row['y']
        adjacencias = [int(adj) for adj in row['adjacencias'].split(',')] if row['adjacencias'] else []

        pontos[id_ponto] = {'nome': id_ponto, 'coordenadas': (x, y), 'adjacencias': adjacencias}

    return pontos