import sys
from mpi4py import MPI
from time import time

import cv2, os
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

def convolucion(img):
    kernel = np.ones((30, 30), np.float32) / 900  # Matriz de convolucion
    dst = cv2.filter2D(img, -1, kernel)

    return dst

image_path = os.getcwd() + '/static/img/'
img = cv2.imread(image_path + '001.jpg', cv2.IMREAD_COLOR)
alt, ancho, canales = img.shape

if alt < size:
    print "Imagen muy pequena"
else:
    start = time()  # Inicia el contador, donde se quiere medir el tiempo


    regionEditada = convolucion(img)
    cv2.imwrite(os.getcwd() + '/images/regionConvolucion.jpg', regionEditada)
    elapsed = time() - start  # Resta del tiempo transcurrido total y donde se inicio el contador

    print "TIEMPO CONVOLUCION: ", elapsed  # Resultado final, en segundos