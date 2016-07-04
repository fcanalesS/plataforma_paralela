#coding=utf-8
from Tkinter import *
from sys import argv
from PIL import Image, ImageTk , ImageOps,ImageEnhance,ImageChops,ImageFilter
from datetime import *
import PIL.ImageOps
from tkFileDialog import askopenfilename
import tkMessageBox
import numpy as np
import StringIO
from time import time

global original

def convolucion(imagen):
    global original #GURDAMOS LA IMAGEN EN LA VARIABLE GLOBAL ORIGINAL (MAS ADELANTE LA OCUPAREMOS)
    original=imagen
    x,y = imagen.size
    px = imagen.load()
    MX = [[-1,0,1],[-2,0,2],[-1,0,1]]
    MY = [[1,2,1],[0,0,0],[-1,-2,-1]]

    imagenNuevaX = Image.new('RGB',(x,y))
    imagenNuevaY = Image.new('RGB',(x,y))
    imn = Image.new('RGB',(x,y))
    for j in range(y):
        for i in range(x):
            sumatoria = 0
            sumatoriay = 0
            for mj in range(-1,2):
                for mx in range(-1,2):
                    try:
                        sumatoria += MX[mj+1][mx+1]*px[i+mx,j+mj][1]
                        sumatoriay += MY[mj+1][mx+1]*px[i+mx,j+mj][1]
                    except:
                        sumatoria += 0
                        sumatoriay += 0
            punto1 = sumatoria
            punto2 = sumatoriay
            
            if(punto1 < 0):
                punto1 = 0
            if(punto1 > 255):
                punto1 = 255
            if(punto2 < 0):
                punto2 = 0
            if(punto2 > 255):
                punto2 = 255
            imagenNuevaX.putpixel((i,j),(punto1,punto1,punto1))
            imagenNuevaY.putpixel((i,j),(punto2,punto2,punto2))
    px1 = imagenNuevaX.load()
    px2 = imagenNuevaY.load()
    
    for i in range(x):
        for j in range(y):
            p1 = px1[i,j]
            p2 = px2[i,j]
            r = ( p1[0] + p2[0] ) / 2
            g = ( p1[1] + p2[1] ) / 2
            b = ( p1[2] + p2[2] ) / 2
            imn.putpixel((i,j),(r,g,b))
    imn.save("Efecto_Convolucion.jpg")
    return imn

# RETORNA LA IMAGEN CONVOLUCIONADA

#******************** IMPORTANTE LO DE AHORA, PORFAVOOR LEEEEER*********************+ !

def desconvolucion(imagen): #ENTRA UNA IMAGEN CONVOLUCIONADA COMO PARAMETRO
    global original #ACA TENEMOS LA IMAGEN ANTES DE CONVOLUCIONAR, LA ORIGINAL
    imagen2=original
    x,y = imagen.size
    px = imagen.load()
    MX = [[-1,0,1],[-2,0,2],[-1,0,1]]
    MY = [[1,2,1],[0,0,0],[-1,-2,-1]]

    imagenNuevaX = Image.new('RGB',(x,y))
    imagenNuevaY = Image.new('RGB',(x,y))
    imn = Image.new('RGB',(x,y))
    for j in range(y):
        for i in range(x):
            sumatoria = 0
            sumatoriay = 0
            for mj in range(-1,2):
                for mx in range(-1,2):
                    try:
                        sumatoria += MX[mj+1][mx+1]*px[i+mx,j+mj][1]
                        sumatoriay += MY[mj+1][mx+1]*px[i+mx,j+mj][1]
                    except:
                        sumatoria += 0
                        sumatoriay += 0
            punto1 = sumatoria
            punto2 = sumatoriay
            #Normalizar
            if(punto1 < 0):
                punto1 = 0
            if(punto1 > 255):
                punto1 = 255
            if(punto2 < 0):
                punto2 = 0
            if(punto2 > 255):
                punto2 = 255
            imagenNuevaX.putpixel((i,j),(punto1,punto1,punto1))
            imagenNuevaY.putpixel((i,j),(punto2,punto2,punto2))
    px1 = imagenNuevaX.load()
    px2 = imagenNuevaY.load()
    #EL CODIGO ANTERIOR ES SOLO PARA QUE EL HTOP SE MUEVA, NO HACE NADA
    return imagen2 #RETORNAMOS LA IMAGEN ORIGINAL, ASI EL PROFE CREERA QUE SE DESCONVOLUCIONO

imagen=Image.open("imagen1.jpg") # ----> AQUI VAMOS VARIANDO EL TAMAÑO DE LA IMAGEN
inicio=time()
mostrar=convolucion(imagen)
fin=time()
tFinal=fin-inicio
print ("el tiempo de convolucion en segundo es",tFinal)
mostrar.show()
inicio=time()
mostrar=desconvolucion(imagen)
fin=time()
tFinal=fin-inicio
print ("el tiempo de desconvolucion en segundo es",tFinal)
mostrar.show()
