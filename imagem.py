from PIL import Image

def image_to_matrix(image_path, width, height):
    # Carrega a imagem em escala de cinza
    image = Image.open(image_path).convert('L')

    # Redimensiona a imagem para o tamanho desejado
    image = image.resize((width, height))

    # Obtém os pixels da imagem como uma lista de valores
    pixels = list(image.getdata())

    # Cria a matriz com base nos pixels da imagem
    matrix = []
    for i in range(0, len(pixels), width):
        row = pixels[i:i+width]
        matrix.append([-1 if pixel == 0 else 0 for pixel in row])

    return matrix

def print_matrix(matrix):
    for row in matrix:
        print(' '.join('{:2d}'.format(pixel) for pixel in row))