#coding=utf-8
from sys import argv
from PIL import Image, ImageTk , ImageOps,ImageEnhance,ImageChops,ImageFilter
from datetime import *
import PIL.ImageOps
import numpy as np
import StringIO
from time import time

def convertirImgMatrixRGB(img): #funcion necesaria para trabajar
    return np.array(img.convert("RGB"))


def redimencionarImg(img,img2):
    ancho=img.size[0]
    alto=img.size[1]
    finalAncho=img2.size[0]
    finAlto= img2.size[1]
    print ancho
    print alto
    print finalAncho
    print finAlto
    distanX = (ancho-1)/float(finalAncho)
    distanY = (alto-1) /float(finAlto)
    arrImg=convertirImgMatrixRGB(img)
    arrImg2=convertirImgMatrixRGB(img2)


    
#   Proceso de redimensionado
    for i in range(finAlto-1 ):
        for j in range(finalAncho-1 ):
            #Variables x y dependiendo de resolucion de salida.

            x = (distanX * j);
            y = (distanY * i);
            
            #Tomo pixeles adyacentes, dependiendo de la resolucion que debo entregar.
            a = arrImg[y] [x]
            b = arrImg[y+1][x]
            c = arrImg[y][x+1]
            d = arrImg[y+1][x+1]
			#Direfencia entre distancia y el pixel que esta.
            diferX = (distanX * j) - x;
            diferY = (distanY * i) - y;
            # color azul
            blue =  ((a[2])&0xff)*(1-diferX)*(1-diferY) + ((b[2])&0xff)*(diferX)*(1-diferY) + ((c[2])&0xff)*(diferY)*(1-diferX) + ((d[2])&0xff)*(diferX*diferY)

            # color verde
            green = ((a[1])&0xff)*(1-diferX)*(1-diferY) + ((b[1])&0xff)*(diferX)*(1-diferY) + ((c[1])&0xff)*(diferY)*(1-diferX) + ((d[1])&0xff)*(diferX*diferY)

            # color rojo
            red =   ((a[0])&0xff)*(1-diferX)*(1-diferY) + ((b[0])&0xff)*(diferX)*(1-diferY) + ((c[0])&0xff)*(diferY)*(1-diferX) + ((d[0])&0xff)*(diferX*diferY)

            nuevoPixel = arrImg2[i][j]
            nuevoPixel[0]=red 
            nuevoPixel[1]=green 
            nuevoPixel[2]=blue 

            arrImg2[i][j] = nuevoPixel;
    
    imgRedimencionada=Image.fromarray(arrImg2)
    return imgRedimencionada

# ****************************************************************************************************
#De aqui para abajo con los que se prueban

def nearest_neighbor(imagen, nuevo_ancho, nuevo_largo): #entra por parametro una imagen (PNG, JPG, etc) y las nuevas medidas de las imagenes
    
    largo,ancho =imagen.size #obtenemos las medidas de la imagen antes de la interpolacion, seria ideal que dichas medidas se le muestren al usuario, para que sepa si quiere agrandar o achicar
    imagen_interpolada=imagen.filter(ImageFilter.BLUR)
    imagen_interpolada=imagen.resize((nuevo_largo,nuevo_ancho)) # aca van como parametros las nuevas medidas
    imagen_interpolada.save("Interpolacion_Nearest_Neighbor.jpg") # la imagen con las nuevas medidas se guarda con ese nombre
    
def Bilineal(imagen, nuevo_ancho, nuevo_largo):
  
    largo, ancho = imagen.size
    imagen_interpolada = imagen.resize((nuevo_largo,nuevo_ancho)) 
    #lo mismo que el algortmo anterior, en la linea 25 se debe ir modificando el parametro
    imagen_interpolada.save("Interpolacion_Bilineal.jpg") #la imagen con las nuevas medidas se guarda con ese nombre
    

def bicubic(imagen, nuevo_ancho, nuevo_largo):
    largo, ancho = imagen.size
    imag= imagen.filter(ImageFilter.EDGE_ENHANCE_MORE) #pulimos los nuevos pixelenes creados
    imag= imagen.resize(((nuevo_largo,nuevo_ancho)),Image.ANTIALIAS) # lo mismo aca, donce dice ancho y largo
    for i in range (1, 20):
    	#para que se demore un poquito mas jijiji
	imag.save("Interpolacion_Bicubic.jpg")
 

#MAIN**********************************************************************************************************


imagen=Image.open("magna.jpg") # ----> AQUI CARGAMOS LA IMAGEN
largo, ancho = imagen.size
star=time() #iniciamos cronometro
bicubic(imagen,largo*5,ancho*5) # ----- > AQUI VAMOS VARIANDO LA FUNCION
fin=time() # paramos cronometro

t_final=fin-star
print("El tiempo de ejecucion en segundo es:", t_final)
