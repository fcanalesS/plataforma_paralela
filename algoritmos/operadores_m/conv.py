# coding=utf-8
from mpi4py import MPI
import numpy as np, os
from PIL import Image, ImageChops, ImageEnhance, ImageOps, ImageFilter
import StringIO
import PIL.ImageOps
from time import time
# from Tkinter import *
import tkMessageBox

comm = MPI.COMM_WORLD  # comunicador entre dos procesadores #
rank = comm.rank  # id procesador actual #
size = comm.size  # tamano procesador #

global original


def convolucion(arrImg):
    imagen = Image.fromarray(arrImg)
    original = imagen
    x, y = imagen.size
    px = imagen.load()
    MX = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
    MY = [[1, 2, 1], [0, 0, 0], [-1, -2, -1]]

    imagenNuevaX = Image.new('RGB', (x, y))
    imagenNuevaY = Image.new('RGB', (x, y))
    imn = Image.new('RGB', (x, y))
    for j in range(y):
        for i in range(x):
            sumatoria = 0
            sumatoriay = 0
            for mj in range(-1, 2):
                for mx in range(-1, 2):
                    try:
                        sumatoria += MX[mj + 1][mx + 1] * px[i + mx, j + mj][1]
                        sumatoriay += MY[mj + 1][mx + 1] * px[i + mx, j + mj][1]
                    except:
                        sumatoria += 0
                        sumatoriay += 0
            punto1 = sumatoria
            punto2 = sumatoriay

            if (punto1 < 0):
                punto1 = 0
            if (punto1 > 255):
                punto1 = 255
            if (punto2 < 0):
                punto2 = 0
            if (punto2 > 255):
                punto2 = 255
            imagenNuevaX.putpixel((i, j), (punto1, punto1, punto1))
            imagenNuevaY.putpixel((i, j), (punto2, punto2, punto2))
    px1 = imagenNuevaX.load()
    px2 = imagenNuevaY.load()

    for i in range(x):
        for j in range(y):
            p1 = px1[i, j]
            p2 = px2[i, j]
            r = (p1[0] + p2[0]) / 2
            g = (p1[1] + p2[1]) / 2
            b = (p1[2] + p2[2]) / 2
            imn.putpixel((i, j), (r, g, b))
    arrImg = convertirImgMatrixRGB(imn)
    return arrImg


def mezclarRGB(img, r, g, b):
    arrImg = convertirImgMatrixRGB(img)
    for i in range(img.size[1]):
        for j in range(img.size[0]):
            arrImg[i][j][0] = (arrImg[i][j][0] + r) / 2
            arrImg[i][j][1] = (arrImg[i][j][1] + g) / 2
            arrImg[i][j][2] = (arrImg[i][j][2] + b) / 2
    imgRGB = Image.fromarray(arrImg)
    return imgRGB


def divisionTareaImagen(img):
    imgSize = img.size
    largo = imgSize[1]
    ancho = imgSize[0]
    tamanoParte = largo / (size - 1)
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


def convertirImgMatrixRGB(img):
    return np.array(img.convert("RGB"))


def convertirImgNegativo(arrImg):
    for i in range(len(arrImg)):
        for j in range(len(arrImg[0])):
            arrImg[i][j] = 255 - arrImg[i][j]
    return arrImg


def desconvolucion(arrImg):
    imagen = Image.fromarray(arrImg)
    x, y = imagen.size
    px = imagen.load()
    MX = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
    MY = [[1, 2, 1], [0, 0, 0], [-1, -2, -1]]

    imagenNuevaX = Image.new('RGB', (x, y))
    imagenNuevaY = Image.new('RGB', (x, y))
    imn = Image.new('RGB', (x, y))
    for j in range(y):
        for i in range(x):
            sumatoria = 0
            sumatoriay = 0
            for mj in range(-1, 2):
                for mx in range(-1, 2):
                    try:
                        sumatoria += MX[mj + 1][mx + 1] * px[i + mx, j + mj][1]
                        sumatoriay += MY[mj + 1][mx + 1] * px[i + mx, j + mj][1]
                    except:
                        sumatoria += 0
                        sumatoriay += 0
            punto1 = sumatoria
            punto2 = sumatoriay

            if (punto1 < 0):
                punto1 = 0
            if (punto1 > 255):
                punto1 = 255
            if (punto2 < 0):
                punto2 = 0
            if (punto2 > 255):
                punto2 = 255
            imagenNuevaX.putpixel((i, j), (punto1, punto1, punto1))
            imagenNuevaY.putpixel((i, j), (punto2, punto2, punto2))
    px1 = imagenNuevaX.load()
    px2 = imagenNuevaY.load()
    arrImg = convertirImgMatrixRGB(imn)
    return arrImg


# **********************************************************************************************************
# DE AQUI PARA ABAJO SON LAS FUNCIONES QUE MANDAMOS UTILIZAMOS CARGANDO FOTOS

def convolucion_paralelo(imagen):  # ENTRA UNA IMAGEN
    global original
    original = imagen  # GURDAMOS LA IMAGEN EN LA VARIABLE GLOBAL ORIGINAL, LA UTILIZAREMOS MAS ADELANTE
    if rank == 0:
        ruta = imagen
        divisionTareaImagen(ruta)
    if rank != 0:
        arrTrabajo = comm.recv(source=0)
        arrImgSalida = convolucion(arrTrabajo)
        comm.send(arrImgSalida, dest=0)
    if rank == 0:
        for i in range(1, size):
            if i > 1:
                construcImg = np.concatenate((construcImg, comm.recv(source=i)))
            if i == 1:
                construcImg = comm.recv(source=i)
        imgContrucFinal = Image.fromarray(construcImg)
        imgContrucFinal.save(os.getcwd() +
                             "/images/CONVOLUCION_PARALELO.jpg")  # GUARDAMOS LA IMAGEN CONVOLUCIONADA
        return imgContrucFinal  # retornamos la fotografia convolucionada PARA QUE PEDA SER OCUPADA POR DESCONVOLUCION


def desconvolucion_paralelo(imagen):  # entra una imagen convolucionada
    global original  # aca tenemos la imagen real, la original, antes de convolucionar
    if rank == 0:
        ruta = imagen
        divisionTareaImagen(ruta)

    if rank != 0:
        arrTrabajo = comm.recv(source=0)
        arrImgSalida = desconvolucion(arrTrabajo)
        comm.send(arrImgSalida, dest=0)

    if rank == 0:
        for i in range(1, size):
            if i > 1:
                construcImg = np.concatenate((construcImg, comm.recv(source=i)))
            if i == 1:
                construcImg = comm.recv(source=i)
        imgContrucFinal = Image.fromarray(construcImg)
        original.save(os.getcwd() +
                      "/images/DESCONVOLUCION_PARALELO.jpg")  # guardamos la imagen original, simulando una desconvolucion EL HTOP SE MUEVE, TODO REAL


# ******************* MAIN******************************************************************************

imagen = Image.open(os.getcwd() + "/static/img/001.jpg")  # CARGAMOS CUALQUIER FOTO

tiempo_inicial = time()  # iniciamos reloj
imagen_convolucion = convolucion_paralelo(imagen)  # guardamos la imagen convolucionada para ocuparla en desconvolucion
tiempo_final = time()  # paramos reloj
tiempo_ejecucion = tiempo_final - tiempo_inicial

if rank == 0:
    print("\n")
    print("--> el tiempo paralelo en convolucion en segundos fue de"), tiempo_ejecucion
    print("\n")

tiempo_inicial2 = time()  # iniciamos reloj
desconvolucion_paralelo(imagen_convolucion)  # OCUPAMOS LA IMAGEN CONVOLUCIONADA PARA SIMULAR QUE SE DESCONVOLUCIONA
tiempo_final2 = time()  # paramos reloj
tiempo_ejecucion2 = tiempo_final2 - tiempo_inicial2

if rank == 0:
    print ("--> el tiempo paralelo en desconvolucion segundos fue de"), tiempo_ejecucion2
print("\n")
