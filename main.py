import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pandas as pd
import entradaSaida as es
import imagem as im
import beacons as bea
import pickle
import os.path

if not os.path.isfile("beacons.pickle"):
    matriz = im.image_to_matrix('Trabalho-grafos/planta_com_vazios.png', 72, 64)
    beacons = bea.Beacons(matriz, 40, 3)
    beacons.calculaBeacons()
    with open("beacons.pickle","wb") as f:
        pickle.dump(beacons, f)
else:
    with open("beacons.pickle", "rb") as f:
        beacons = pickle.load(f)