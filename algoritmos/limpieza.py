import os
import cv2
import numpy as np
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()


def unirImagen(n):
    if n > 0:
        while rank < n or rank == 0:
            i = rank * 2
            # Cargando imagenes
            img1 = cv2.imread(os.getcwd() + '/images/regionEditada_' + str(i) + ".jpg", cv2.IMREAD_COLOR)
            img2 = cv2.imread(os.getcwd() + '/images/regionEditada_' + str(i + 1) + ".jpg", cv2.IMREAD_COLOR)
            # Guardando datos
            alt1, ancho1, canales1 = img1.shape
            alt2, ancho2, canales2 = img2.shape
            # Creando imagen vacia
            img = np.zeros((alt1 + alt2, ancho1, 3), np.uint8)
            # Pegando en la imagen vacia las dos imagenes
            img[0:alt1, 0:ancho1] = img1
            img[alt1:alt1 + alt2, 0:ancho1] = img2
            # Borramos los archivos ya usados
            os.system('rm ' + os.getcwd() + '/images/regionEditada_' + str(i) + '.jpg')
            os.system('rm ' + os.getcwd() + '/images/regionEditada_' + str(i + 1) + '.jpg')
            # Comprobando que no se sobreesciba un archivo
            while existe(os.getcwd() + '/images/regionEditada_' + str(rank) + '.jpg'):
                a = 0
            # Guardando imagen final
            cv2.imwrite(os.getcwd() + '/images/regionEditada_' + str(rank) + ".jpg", img)
            # Comprobando que se borren todos los archivos antes de iniciar la nueva ronda
            r = n
            while r < n * 2:
                if not existe(os.getcwd() + '/images/regionEditada_' + str(r) + '.jpg'):
                    r += 1
            n //= 2


def existe(archivo):
    try:
        fichero = open(archivo)
        fichero.close()
        return True
    except:
        return False


unirImagen(size // 2)
