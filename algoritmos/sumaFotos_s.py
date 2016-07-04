import numpy as np
import time
from PIL import Image
import sys
inicio = time.time()

#Nivel de transparencia de imagen 1, para que queden igualmete mezcladas se debe usar un alfa=0.5
ALFA=0.5

def convertirImgMatrixRGB(img):
    return np.array(img.convert("RGB"))

#mezcla 2 imagenes en una,el alfa es usado para definir el nivel de transparencia de las imagenes.
def sumarImagenes(fpImg1,fpImg2,alfa):

    img1=Image.open(fpImg1)
    img2=Image.open(fpImg2).resize(img1.size) #redimensiono la segunda imagen al tamano del fondo
                                              #el fondo rules!.
    arrImg1=convertirImgMatrixRGB(img1)
    arrImg2=convertirImgMatrixRGB(img2)
    for i in range(img1.size[1]):
        for j in range(img1.size[0]):
            sumaPixel= (arrImg1[i][j]*(1-alfa))+(arrImg2[i][j]*(alfa))
            arrImg1[i][j]=sumaPixel
    imgSuma=Image.fromarray(arrImg1)
    return imgSuma

def main():
    #ahora en vez de pasar la imagen en memoria a la funcion
    #se le pasa el filepath y la funcion se encarga de cargar en memoria.
#    img1 = array(Image.open(sys.argv))
#    img2 = array(Image.open(sys.argv))
    imagenSumada=sumarImagenes('imagen1.jpg', 'imagensuma.jpg',ALFA)
#    imagenSumada=sumarImagenes(img1,img2,ALFA)
    imagenSumada.save('suma.jpg')
    print ""
    print "Serial Time : "+str(time.time()-inicio)+" seconds"

main()

