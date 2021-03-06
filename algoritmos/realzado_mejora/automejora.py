from mpi4py import MPI
import cv2, os
from time import time

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

def automejora(img):
    b, g, r = cv2.split(img)

    equb = cv2.equalizeHist(b)
    equg = cv2.equalizeHist(g)
    equr = cv2.equalizeHist(r)

    res_bgr = cv2.merge((equb, equg, equr))

    return res_bgr

image_path = os.getcwd() + '/static/img/'
img = cv2.imread(image_path + '001.jpg', cv2.IMREAD_COLOR)
alt, ancho, canales = img.shape

if alt < size:
    print "Imagen muy pequena"
else:
    start_time = time()
    if rank == 0:
        region = img[(alt / size) * rank:(alt / size) * (rank + 1) + 25, 0:ancho]
    else:
        region = img[(alt / size) * rank - 25:(alt / size) * (rank + 1) + 25, 0:ancho]
    regionEditada = automejora(region)
    alt, ancho, canales = regionEditada.shape
    if rank == 0:
        regionEditada = regionEditada[0:alt - 25, 0:ancho]
    else:
        regionEditada = regionEditada[25:alt - 25, 0:ancho]
    cv2.imwrite(os.getcwd() + '/images/regionEditada_' + str(rank) + '.jpg', regionEditada)
    elapsed_time = time() - start_time
    print "Elapsed time: %0.10f secconds. " % elapsed_time

