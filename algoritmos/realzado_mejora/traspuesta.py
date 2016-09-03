import sys
from mpi4py import MPI
from time import time
import cv2, os
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()


def traspuesta(image):
    rows, cols, _ = img.shape

    # M = cv2.getRotationMatrix2D((cols / 2, rows / 2), int(sys.argv[1]), 0.5)
    # dst = cv2.warpAffine(img, M, (cols, rows))

    height = image.shape[0]
    width = image.shape[1]
    height_big = height * 2
    width_big = width * 2
    image_big = cv2.resize(image, (width_big, height_big))
    image_center = (width_big / 2, height_big / 2)  # rotation center
    rot_mat = cv2.getRotationMatrix2D(image_center, int(sys.argv[1]), 1.0)
    result = cv2.warpAffine(image_big, rot_mat, (width_big, height_big), flags=cv2.INTER_LINEAR)
    return result

    #return dst


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
    regionEditada = traspuesta(region)
    alt, ancho, canales = regionEditada.shape
    if rank == 0:
        regionEditada = regionEditada[0:alt - 25, 0:ancho]
    else:
        regionEditada = regionEditada[25:alt - 25, 0:ancho]
    cv2.imwrite(os.getcwd() + '/images/traspuesta/regionEditada_' + str(rank) + ".jpg", regionEditada)
    elapsed = time() - start
    print "TIEMPO TRASPOSE: ", elapsed
