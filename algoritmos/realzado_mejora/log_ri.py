# coding=utf-8
from mpi4py import MPI
import numpy as np
from PIL import Image, ImageChops, ImageEnhance, ImageOps, ImageFilter
import StringIO
import PIL.ImageOps
from time import time
import cv2, os
import Image

comm = MPI.COMM_WORLD  # comunicador entre dos procesadores #

rank = comm.rank  # id procesador actual #
size = comm.size  # tamano procesador #


# largo=imgSize[1]
# ancho=imgSize[0]
# print "largo :",largo
# print "Ancho :",ancho



def blur(arrImg):
    final = Image.fromarray(arrImg)
    new_image = final.filter(ImageFilter.GaussianBlur)
    arrImg = convertirImgMatrixRGB(new_image)
    return arrImg


def log(arrImg):
    final = Image.fromarray(arrImg)
    new_image = final.filter(ImageFilter.GaussianBlur)
    new_image = new_image.filter(ImageFilter.FIND_EDGES)
    arrImg = convertirImgMatrixRGB(new_image)
    return arrImg


def convertirImgMatrixRGB(img):
    return np.array(img.convert("RGB"))


# funcion que recibe la ruta de imagen y distribuye los trozos horizontales a cada procesador excepto el cero
def divisionTareaImagen(img):
    # img=Image.open(ruta)
    imgSize = img.size
    largo = imgSize[1]
    ancho = imgSize[0]
    tamanoParte = largo / (size)  # (size-1) es para no incluir el procesador cero
    xInicio = 0
    yInicio = 0
    tamPar = tamanoParte
    for i in range(1, size):
        parteImgEnvio = img.crop((xInicio, yInicio, ancho, tamPar))
        tamPar = tamPar + tamanoParte
        yInicio = yInicio + tamanoParte
        rutaSalida = "photoCut" + str(i) + ".jpg"
        parteImgEnvio.save(rutaSalida)
        arrImg = convertirImgMatrixRGB(parteImgEnvio)
        comm.send(arrImg, dest=i)


def sepia_final(imagen):
    if rank == 0:
        # ruta="magna.jpg"
        divisionTareaImagen(imagen)
    if rank != 0:
        arrTrabajo = comm.recv(
            source=0)  # cada procesador recibe un arreglo RGB que contiene un trozo horizontal de la imagen

        # arrImgSalida=log(arrTrabajo)
        arrImgSalida = blur(arrTrabajo)
        comm.send(arrImgSalida, dest=0)
    if rank == 0:  # recibe los arreglos y los junta uno abajo del otro
        for i in range(1, size):
            if i > 1:
                construcImg = np.concatenate((construcImg, comm.recv(source=i)))
            if i == 1:
                construcImg = comm.recv(source=i)
        imgContrucFinal = Image.fromarray(construcImg)
        imgContrucFinal.save(os.getcwd() + "/images/Logfinal.jpg")


imagen = Image.open(os.getcwd() + '/static/img/001.jpg')
tiempo_inicial = time()  # inicio toma tiempo
sepia_final(imagen)
tiempo_final = time()  # termino toma tiempo
tiempo_ejecucion = tiempo_final - tiempo_inicial
print tiempo_ejecucion
