import numpy
from PIL import Image,ImageChops, ImageEnhance, ImageOps, ImageFilter
from scipy import misc
from scipy import ndimage
import math
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image,ImageChops, ImageEnhance, ImageOps, ImageFilter
import StringIO
import PIL.ImageOps 
import time
from mpi4py import MPI
from scipy.misc import toimage

comm = MPI.COMM_WORLD  # comunicador entre dos procesadores #

rank = comm.rank     # id procesador actual #
size = comm.size     # tamano procesador #

#foto=Image.open("magna.jpg")
#foto2.show()


def convertirImgMatrixRGB(img):
   return np.array(img.convert("RGB"))

def convertirImgNegativo(arrImg):
   for i in range(len(arrImg)): #largo
      for j in range(len(arrImg[0])):  #ancho
         arrImg[i][j] = 255-arrImg[i][j]
   return arrImg

def divisionTareaImagen(img):
   img = Image.open(img)
   imgSize=img.size
   largo=imgSize[1]
   ancho=imgSize[0]
   tamanoParte=largo/(size-1)  #(size-1) es para no incluir el procesador cero
   xInicio=0
   yInicio=0
   tamPar=tamanoParte
   for i in range(1,size):
      parteImgEnvio=img.crop((xInicio,yInicio,ancho,tamPar))
      tamPar=tamPar+tamanoParte
      yInicio=yInicio+tamanoParte
      rutaSalida="photoCut"+str(i)+".jpg"
      parteImgEnvio.save(rutaSalida)
      arrImg=convertirImgMatrixRGB(parteImgEnvio)
      comm.send(arrImg,dest=i)



def ifftExample():
   shift = 4
   spectrum = numpy.zeros((513,513))
   spectrum[256,256] = 1
   spectrum[256,256 + shift] = 1
   spectrum[256,256 - shift] = 1

   plt.clf()
   plt.imshow(spectrum, cmap=plt.cm.gray)
   plt.show()


   A = numpy.fft.ifft2(spectrum)
   img = numpy.array([[numpy.absolute(x) for x in row] for row in A])

   plt.clf()
   plt.imshow(img, cmap=plt.cm.gray)
   plt.show()


def espectro(arrImg):
   #img=Image.fromarray(arrImg)
   A = ndimage.imread(arrImg, flatten=True)
   unshiftedfft = numpy.fft.fft2(A)
   spectrum = numpy.log10(numpy.absolute(unshiftedfft) + numpy.ones(A.shape))
   shiftedFFT = numpy.fft.fftshift(numpy.fft.fft2(A))
   spectrum = numpy.log10(numpy.absolute(shiftedFFT) + numpy.ones(A.shape))
   plt.imshow(spectrum)
   plt.title('MAGNITUD DEL ESPECTRO LUMINOZO')
   plt.show()
    
def fourierSpectrumExample2(filename):
   A = ndimage.imread(filename, flatten=True) #A no es una foto JPG ni nada de eso
   unshiftedfft = numpy.fft.fft2(A)
   spectrum = numpy.log10(numpy.absolute(unshiftedfft) + numpy.ones(A.shape))
   shiftedFFT = numpy.fft.fftshift(numpy.fft.fft2(A))
   spectrum = numpy.log10(numpy.absolute(shiftedFFT) + numpy.ones(A.shape))
   spectrum=toimage(spectrum)
   spectrum.save("FOURIER_PARALELO.jpg")

def fourierSpectrumExample(filename):
   #A = ndimage.imread(filename, flatten=True)
   A=filename
   unshiftedfft = numpy.fft.fft2(A)
   spectrum = numpy.log10(numpy.absolute(unshiftedfft) + numpy.ones(A.shape))
   #misc.imsave("imagen_difusa.png", spectrum)

   shiftedFFT = numpy.fft.fftshift(numpy.fft.fft2(A))
   spectrum = numpy.log10(numpy.absolute(shiftedFFT) + numpy.ones(A.shape))
   #misc.imsave("imagen_normalizada.png" , spectrum)
   #plt.imshow(spectrum)
   #plt.title('Magnitude Spectrum')
   #plt.show()
   spectrum=toimage(spectrum) #AQU ESTA LA CLAVE DEL EXITOO !!
   arrImg=convertirImgMatrixRGB(spectrum)
   return arrImg


def furier_paralelo():
   starting_point=time.time()
   if rank==0:
      espectro("imagen1.jpg")
      ruta =("imagen1.jpg")
      divisionTareaImagen(ruta)
   if rank!=0:
      arrTrabajo=comm.recv(source=0)    #cada procesador recibe un arreglo RGB que contiene un trozo horizontal de la imagen
      arrImgSalida=fourierSpectrumExample(arrTrabajo)
      comm.send(arrImgSalida,dest=0)
   if rank==0 :       #recibe los arreglos y los junta uno abajo del otro
      for i in range(1,size):
         if i > 1:
            construcImg = np.concatenate((construcImg,comm.recv(source=i)))
         if i == 1:
            construcImg = comm.recv(source=i)
            imgContrucFinal=Image.fromarray(construcImg)
            fourierSpectrumExample2(ruta)

#*************************MAIN( )****************************************
   elapsed_time=time.time()-starting_point
   print ""
   print "Tiempo paralelo [s]: " + str(elapsed_time)
   print ""
furier_paralelo() #TaPasao 1313
