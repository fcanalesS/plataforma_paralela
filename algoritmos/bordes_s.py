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


def bordes(imagen_original, mascara):
    
    x, y = imagen_original.size
    pos = imagen_original.load()
    nueva_imagen = Image.new("RGB", (x,y))
    pos_nueva = nueva_imagen.load()
    for i in range(x):
        for j in range(y):
            total = 0
            for n in range(i-1, i+2):
                for m in range(j-1, j+2):
                    if n >= 0 and m >= 0 and n < x and m < y:
                        total += mascara[n - (i - 1)][ m - (j - 1)] * pos[n, m][0]
            pos_nueva[i, j] = (total, total, total)
    nueva_imagen.save("BORDE_SECUENCIAL.png")
    
    return nueva_imagen


    #**************** MAIN()

mascara1 = [[-1,0,1],[-2,0,2],[-1,0,1]]
foto=Image.open("imagen1.jpg")
final=bordes(foto,mascara1)
final.show()
