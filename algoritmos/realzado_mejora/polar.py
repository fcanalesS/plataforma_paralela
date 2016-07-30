# coding=utf-8
from PIL import Image
from time import time  # libreria para tomar tiempos
from numpy import *  # para pasar a array la imagen
from scipy.ndimage import geometric_transform  # para trabajar deformaciones
from scipy.misc import imsave
import matplotlib.pyplot as plt
import cv2, os
import Image


def polar_warp(im, sz, r):
    # Deformar una imagen para una versión polar cuadrada

    h, w = im.shape[:2]

    def polar_2_rect(xy):
        # Convertir coordenadas polares a en
        #	la imagen original para transformar geométrica

        x, y = float(xy[1]), float(xy[0])
        theta = 0.5 * arctan2(x - sz / 2, y - sz / 2)
        R = sqrt((x - sz / 2) * (x - sz / 2) + (y - sz / 2) * (y - sz / 2)) - r

        return (2 * h * R / (sz - 2 * r), w / 2 + theta * w / pi + pi / 2)

    # color de la imagen se deforma cada canal, si no hay una sola
    if len(im.shape) == 3:
        warped = zeros((sz, sz, 3))
        for i in range(3):
            warped[:, :, i] = geometric_transform(im[:, :, i], polar_2_rect, output_shape=(sz, sz), mode='nearest')
    else:
        warped = geometric_transform(im, polar_2_rect, output_shape=(sz, sz), mode='nearest')

    return warped


if __name__ == "__main__":
    tiempo_inicial = time()  # incio conteo
    im = array(Image.open(os.getcwd() + '/static/img/001.jpg'))  # abro imagen
    h, w = im.shape[:2]
    # Voltear vertical para hacer más fácil para las matemáticas
    im = flipud(im)
    # deforma imagen
    wim = uint8(polar_warp(im, h, 5))
    tiempo_final = time()  # fin del conteo
    tiempo_ejecucion = tiempo_final - tiempo_inicial
    # guardar imagen
    imsave(os.getcwd() + '/images/polar.jpg', wim)
    # plt.imshow(wim)  # se muestra la imagen polar como grafico
    # plt.show()
    print tiempo_ejecucion
