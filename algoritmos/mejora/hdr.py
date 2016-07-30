from mpi4py import MPI
from time import time

import cv2, os
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()


file_path = os.getcwd() + '/images/HDR'


imgs = os.listdir(file_path)
imgs.sort()

img_fn = imgs
img_list = [cv2.imread(file_path + '/' + fn) for fn in img_fn]

start = time()
merge_mertens = cv2.createMergeMertens()
res_mertens = merge_mertens.process(img_list)

# Convert datatype to 8-bit and save
res_mertens_8bit = np.clip(res_mertens*255, 0, 255).astype('uint8')

cv2.imwrite(file_path + '/' + "hdr.jpg", res_mertens_8bit)
elapsed = time() - start

print "TIEMPO HDR: ", elapsed