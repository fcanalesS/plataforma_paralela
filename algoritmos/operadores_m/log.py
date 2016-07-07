# coding=utf-8
import cv2
import numpy as np
import os
from time import time

tiempo_inicial = time()

kernel_size = 3
scale = 1
delta = 0
ddepth = cv2.CV_16S

### Se carga la imagen
img = cv2.imread(os.getcwd() + '/static/img/001.jpg')

### Se elimina el ruido mediante un desenfoque o filtro gaussiano, donde:
# img: imagen de entrada
# (3,3): anchura y altura del kernel gaussiano (pueden ser distintos pero deben ser positivos e impares)
# 0: desviación estándar del kernel gaussiano en la dirección X (si es igual a cero, tanto X como Y son ceros)
img = cv2.GaussianBlur(img,(3,3),0)

### Se convierte la imagen de un espacio de color a otro, en este caso es a "escala de grises"
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

### Se aplica un operador de Laplace a la imagen en escala de grises, donde:
# gray: imagen de origen
# ddepth: profundidad deseada de la imagen de destino
# ksize: tamaño de la abertura usada para calcular la segunda derivada (debe ser positivo e impar)
# scale: factor de escala opcional para los valores calculados de Laplace (por defecto no se aplica ninguna escala)
# delta: valor delta opcional que se añade a los resultados antes de almacenarlos
gray_lap = cv2.Laplacian(gray,ddepth,ksize = kernel_size,scale = scale,delta = delta)

### Se Calculan los valores absolutos, y convierte el resultado a 8 bits, donde:
# gray_lap: matriz de entrada (donde se calculó el Laplaciano)
dst = cv2.convertScaleAbs(gray_lap)

### Se muestra por pantalla la imagen con el efecto aplicado finalmente
cv2.imwrite(os.getcwd() + '/images/laplacian.jpg', dst)

tiempo_final = time()
tiempo_ejecucion = tiempo_final - tiempo_inicial
print("El tiempo (en seg) es de: "), tiempo_ejecucion

### Se mantiene la pantalla en ejecucion hasta que el usuario presione la tecla cero (0)
cv2.waitKey(0)
cv2.destroyAllWindows()