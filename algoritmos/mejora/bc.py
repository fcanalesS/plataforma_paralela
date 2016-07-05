import sys
from mpi4py import MPI
from time import time

import cv2, os
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()


def brilloContraste(img):
    img2hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(img2hsv)

    s = cv2.multiply(s, np.array([float(sys.argv[1])]))
    v = cv2.multiply(v, np.array([float(sys.argv[2])]))

    res = cv2.merge((h, s, v))

    result = cv2.cvtColor(res, cv2.COLOR_HSV2BGR)

    return result


image_path = os.getcwd() + '/static/img/'
img = cv2.imread(image_path + '001.jpg', cv2.IMREAD_COLOR)
alt, ancho, canales = img.shape

if alt < size:
    print "Imagen muy pequena"
else:
    start = time()
    if rank == 0:
        region = img[(alt / size) * rank:(alt / size) * (rank + 1) + 25, 0:ancho]
    else:
        region = img[(alt / size) * rank - 25:(alt / size) * (rank + 1) + 25, 0:ancho]
    regionEditada = brilloContraste(region)
    alt, ancho, canales = regionEditada.shape
    if rank == 0:
        regionEditada = regionEditada[0:alt - 25, 0:ancho]
    else:
        regionEditada = regionEditada[25:alt - 25, 0:ancho]
    cv2.imwrite(os.getcwd() + '/images/regionEditada_' + str(rank) + ".jpg", regionEditada)
    elapsed = time() - start
    print "TIEMPO SEC BC: ", elapsed
