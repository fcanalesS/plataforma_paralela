from mpi4py import MPI
import numpy as np
import ImageFilter
from numpy import array, shape, reshape, zeros, transpose
from PIL import Image, ImageChops, ImageOps
import StringIO
import time
import math
import cv2, os
import Image

comm = MPI.COMM_WORLD  # comunicador entre dos procesadores #
rank = comm.rank  # id procesador actual #
size = comm.size  # tamano procesador #


def convertirImgMatrixRGB(img):
    return np.array(img.convert("RGB"))


# resultado esta dado en mascara 1

def bordes(imagen_original, mascara):
    imagen_original = Image.fromarray(imagen_original)
    x, y = imagen_original.size
    pos = imagen_original.load()
    nueva_imagen = Image.new("RGB", (x, y))
    pos_nueva = nueva_imagen.load()
    for i in range(x):
        for j in range(y):
            total = 0
            for n in range(i - 1, i + 2):
                for m in range(j - 1, j + 2):
                    if n >= 0 and m >= 0 and n < x and m < y:
                        total += mascara[n - (i - 1)][m - (j - 1)] * pos[n, m][0]
            pos_nueva[i, j] = (total, total, total)
    # nueva_imagen.save("mascara.png")
    nueva_imagen = convertirImgMatrixRGB(nueva_imagen)
    return nueva_imagen


def divisionTareaImagen(ruta):
    img = Image.open(ruta)
    imgSize = img.size
    largo = imgSize[1]
    ancho = imgSize[0]
    tamanoParte = largo / (size - 1)  # (size-1) es para no incluir el procesador cero
    xInicio = 0
    yInicio = 0
    tamPar = tamanoParte
    for i in range(1, size):
        parteImgEnvio = img.crop((xInicio, yInicio, ancho, tamPar))
        tamPar = tamPar + tamanoParte
        yInicio = yInicio + tamanoParte
        # rutaSalida = "photoCut" + str(i) + ".png"
        # parteImgEnvio.save(rutaSalida)
        arrImg = convertirImgMatrixRGB(parteImgEnvio)
        comm.send(arrImg, dest=i)


def main():
    starting_point = time.time()

    if rank == 0:
        ruta = os.getcwd() + '/static/img/001.jpg'  # CARGAR LA IMAGEN QUE SE DESEA
        divisionTareaImagen(ruta)

    if rank != 0:
        arrTrabajo = comm.recv(
            source=0)  # cada procesador recibe un arreglo RGB que contiene un trozo horizontal de la imagen
        mascara1 = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
        arrImgSalida = bordes(arrTrabajo,
                              mascara1)  # enviar el arreglo RGB a transformarlo en arreglo negativo de la imagen
        comm.send(arrImgSalida, dest=0)

    if rank == 0:  # recibe los arreglos y los junta uno abajo del otro
        for i in range(1, size):
            if i > 1:
                construcImg = np.concatenate((construcImg, comm.recv(source=i)))
            if i == 1:
                construcImg = comm.recv(source=i)
        imgContrucFinal = Image.fromarray(construcImg)
        imgContrucFinal.save(os.getcwd() + "/images/BORDE_PARALELO.jpg")

        elapsed_time = time.time() - starting_point
        print ""
        print "Tiempo paralelo [s]: " + str(elapsed_time)
        print ""


main()
