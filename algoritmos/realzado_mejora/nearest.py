# coding=utf-8
import sys
from PIL import Image, ImageTk, ImageOps, ImageEnhance, ImageChops, ImageFilter
from datetime import *
import PIL.ImageOps
import numpy as np
import StringIO
from time import time
from mpi4py import MPI
import cv2, os
import Image

comm = MPI.COMM_WORLD  # comunicador entre dos procesadores #
rank = comm.Get_rank()  # id procesador actual #
size = comm.Get_size()  # tamano procesador #

def convertirImgMatrixRGB(img):  # funcion necesaria para trabajar
    return np.array(img.convert("RGB"))


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
        # rutaSalida="photoCut"+str(i)+".jpg"
        # parteImgEnvio.save(rutaSalida)
        arrImg = convertirImgMatrixRGB(parteImgEnvio)
        comm.send(arrImg, dest=i)


def convertirImgMatrixRGB(img):
    return np.array(img.convert("RGB"))


def convertirImgNegativo(arrImg):
    for i in range(len(arrImg)):
        for j in range(len(arrImg[0])):
            arrImg[i][j] = 255 - arrImg[i][j]
    return arrImg


def redimencionarImg(img, img2):
    ancho = img.size[0]
    alto = img.size[1]
    finalAncho = img2.size[0]
    finAlto = img2.size[1]
    print ancho
    print alto
    print finalAncho
    print finAlto
    distanX = (ancho - 1) / float(finalAncho)
    distanY = (alto - 1) / float(finAlto)
    arrImg = convertirImgMatrixRGB(img)
    arrImg2 = convertirImgMatrixRGB(img2)

    #   Proceso de redimensionado
    for i in range(finAlto - 1):
        for j in range(finalAncho - 1):
            # Variables x y dependiendo de resolucion de salida.

            x = (distanX * j);
            y = (distanY * i);

            # Tomo pixeles adyacentes, dependiendo de la resolucion que debo entregar.
            a = arrImg[y][x]
            b = arrImg[y + 1][x]
            c = arrImg[y][x + 1]
            d = arrImg[y + 1][x + 1]
            # Direfencia entre distancia y el pixel que esta.
            diferX = (distanX * j) - x;
            diferY = (distanY * i) - y;
            # color azul
            blue = ((a[2]) & 0xff) * (1 - diferX) * (1 - diferY) + ((b[2]) & 0xff) * (diferX) * (1 - diferY) + ((c[
                                                                                                                     2]) & 0xff) * (
                                                                                                               diferY) * (
                                                                                                               1 - diferX) + (
                                                                                                                             (
                                                                                                                             d[
                                                                                                                                 2]) & 0xff) * (
                                                                                                                             diferX * diferY)

            # color verde
            green = ((a[1]) & 0xff) * (1 - diferX) * (1 - diferY) + ((b[1]) & 0xff) * (diferX) * (1 - diferY) + ((c[
                                                                                                                      1]) & 0xff) * (
                                                                                                                diferY) * (
                                                                                                                1 - diferX) + (
                                                                                                                              (
                                                                                                                              d[
                                                                                                                                  1]) & 0xff) * (
                                                                                                                              diferX * diferY)

            # color rojo
            red = ((a[0]) & 0xff) * (1 - diferX) * (1 - diferY) + ((b[0]) & 0xff) * (diferX) * (1 - diferY) + ((c[
                                                                                                                    0]) & 0xff) * (
                                                                                                              diferY) * (
                                                                                                              1 - diferX) + (
                                                                                                                            (
                                                                                                                            d[
                                                                                                                                0]) & 0xff) * (
                                                                                                                            diferX * diferY)

            nuevoPixel = arrImg2[i][j]
            nuevoPixel[0] = red
            nuevoPixel[1] = green
            nuevoPixel[2] = blue

            arrImg2[i][j] = nuevoPixel;

    imgRedimencionada = Image.fromarray(arrImg2)
    return imgRedimencionada


# *****************************************************************************************************
# ****************************************************************************************************
# De aqui para abajo son los que se prueban


def nearest_neighbor(arrImg, nuevo_ancho,
                     nuevo_largo):  # entra por parametro una imagen (PNG, JPG, etc) y las nuevas medidas de las imagenes
    imagen = Image.fromarray(arrImg)
    # largo,ancho =imagen.size #obtenemos las medidas de la imagen antes de la interpolacion, seria ideal que dichas medidas se le muestren al usuario, para que sepa si quiere agrandar o achicar
    imagen_interpolada = imagen.filter(ImageFilter.BLUR)
    imagen_interpolada = imagen.resize((nuevo_largo, nuevo_ancho))  # aca van como parametros las nuevas medidas
    arrImg = convertirImgMatrixRGB(imagen_interpolada)
    return arrImg
    # imagen_interpolada.save("Interpolacion_Nearest_Neighbor.jpg") # la imagen con las nuevas medidas se guarda con ese nombre


def Bilineal(arrImg, nuevo_ancho, nuevo_largo):
    imagen = Image.fromarray(arrImg)
    # largo, ancho = imagen.size
    imagen_interpolada = imagen.resize((nuevo_largo, nuevo_ancho))
    arrImg = convertirImgMatrixRGB(imagen_interpolada)
    return arrImg
    # lo mismo que el algortmo anterior, en la linea 25 se debe ir modificando el parametro
    # imagen_interpolada.save("Interpolacion_Bilineal.jpg") #la imagen con las nuevas medidas se guarda con ese nombre


def bicubic(arrImg, nuevo_ancho, nuevo_largo):
    imagen = Image.fromarray(arrImg)
    largo, ancho = imagen.size
    imag = imagen.filter(ImageFilter.EDGE_ENHANCE_MORE)  # pulimos los nuevos pixelenes creados
    imag = imagen.resize(((nuevo_largo, nuevo_ancho)), Image.ANTIALIAS)  # lo mismo aca, donce dice ancho y largo
    for i in range(1, 8):
        # para que se demore un poquito mas jijiji

        arrImg = convertirImgMatrixRGB(imag)
    imgRedimencionada = redimencionarImg(imagen, imagen)
    imag.save("Interpolacion_Bicubic.jpg")
    return arrImg


# ALGORITMOS PARALELOS QUE SE MANDAN A LLAMARA EN EL MAIN***********************************************************************************************************


# *********************************** MAIN () ***************************

def nearest_paralelo(imagen, ancho, largo):  # ENTRA UNA IMAGEN

    if rank == 0:
        ruta = imagen
        divisionTareaImagen(ruta)
    if rank != 0:
        arrTrabajo = comm.recv(source=0)
        arrImgSalida = nearest_neighbor(arrTrabajo, ancho, largo)
        comm.send(arrImgSalida, dest=0)
    if rank == 0:
        for i in range(1, size):
            if i > 1:
                construcImg = np.concatenate((construcImg, comm.recv(source=i)))
            if i == 1:
                construcImg = comm.recv(source=i)
        imgContrucFinal = Image.fromarray(construcImg)
        imgContrucFinal.save(os.getcwd() + "/images/REDIMENCION_NEAREST.jpg")  # GUARDAMOS LA IMAGEN


def bilineal_paralelo(imagen, ancho, largo):  # ENTRA UNA IMAGEN

    if rank == 0:
        ruta = imagen
        divisionTareaImagen(ruta)
    if rank != 0:
        arrTrabajo = comm.recv(source=0)
        arrImgSalida = Bilineal(arrTrabajo, ancho, largo)
        comm.send(arrImgSalida, dest=0)
    if rank == 0:
        for i in range(1, size):
            if i > 1:
                construcImg = np.concatenate((construcImg, comm.recv(source=i)))
            if i == 1:
                construcImg = comm.recv(source=i)
        imgContrucFinal = Image.fromarray(construcImg)
        imgContrucFinal.save("REDIMENCION_BILINEAL.jpg")  # GUARDAMOS LA IMAGEN


def bicubic_paralelo(imagen, ancho, largo):  # ENTRA UNA IMAGEN

    if rank == 0:
        ruta = imagen
        divisionTareaImagen(ruta)
    if rank != 0:
        arrTrabajo = comm.recv(source=0)
        arrImgSalida = Bilineal(arrTrabajo, ancho, largo)
        comm.send(arrImgSalida, dest=0)
    if rank == 0:
        for i in range(1, size):
            if i > 1:
                construcImg = np.concatenate((construcImg, comm.recv(source=i)))
            if i == 1:
                construcImg = comm.recv(source=i)
        imgContrucFinal = Image.fromarray(construcImg)
        imagenFinal = imgContrucFinal.resize((ancho, largo))
        imagenFinal.save("REDIMENCION_BICUBIC.jpg")  # GUARDAMOS LA IMAGEN


# MAIN******************************************************************************************************
image_path = os.getcwd() + '/static/img/'
img = cv2.imread(image_path + '001.jpg', cv2.IMREAD_COLOR)
alt, ancho, canales = img.shape

img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
pil_im = Image.fromarray(img)

imagen = pil_im  # ----> CARGAMOS CUALQUIER IMAGEN

star = time()  # iniciamos cronometro

nearest_paralelo(imagen, sys.argv[1], sys.argv[1])  # ----- > AQUI VAMOS VARIANDO LA FUNCION Y LOS TAMAÑOS

fin = time()  # paramos cronometro

t_final = fin - star  # timepo final
print("El tiempo de ejecucion en segundo es:", t_final)
