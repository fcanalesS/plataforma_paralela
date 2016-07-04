from mpi4py import MPI
import cv2, os
from time import time

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()


def negativo(img):
    result = abs(255 - img)

    return result

image_path = os.getcwd() + '/images/'
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
    regionEditada = negativo(region)
    alt, ancho, canales = regionEditada.shape
    if rank == 0:
        regionEditada = regionEditada[0:alt - 25, 0:ancho]
    else:
        regionEditada = regionEditada[25:alt - 25, 0:ancho]
    cv2.imwrite(os.getcwd() + '/images/regionEditada_' + str(rank) + ".jpg", regionEditada)
    elapsed_time = time() - start

    print "TIEMPO SEGUNDOS: ", elapsed_time
