import numpy
from scipy import misc
from scipy import ndimage
import math
import matplotlib.pyplot as plt
from scipy.misc import toimage

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


def fourierSpectrumExample(filename):
   A = ndimage.imread(filename, flatten=True) #A no es una foto JPG ni nada de eso
   unshiftedfft = numpy.fft.fft2(A)
   spectrum = numpy.log10(numpy.absolute(unshiftedfft) + numpy.ones(A.shape))
   misc.imsave("imagen_difusa.png", spectrum)

   shiftedFFT = numpy.fft.fftshift(numpy.fft.fft2(A))
   spectrum = numpy.log10(numpy.absolute(shiftedFFT) + numpy.ones(A.shape))
   misc.imsave("imagen_normalizada.png" , spectrum)
   plt.imshow(spectrum)
   plt.title('Magnitude Spectrum')
   plt.show()
   spectrum=toimage(spectrum)
   spectrum.save("FOURIER_SECUENCIAL.jpg")


fourierSpectrumExample('imagen1.jpg')

