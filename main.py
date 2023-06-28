import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pandas as pd
import entradaSaida as es
import imagem as im
import beacons as bea

matriz = im.image_to_matrix('Trabalho-grafos/planta_com_vazios.png', 72, 64)
beacons = bea.Beacons(matriz, 40, 3)
beacons.calculaBeacons()
print()
im.print_matrix(beacons.matriz)
print()
im.print_matrix(beacons.beacons)