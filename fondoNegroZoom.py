import numpy as np
import tifffile as tiff
import matplotlib.pyplot as plt

arr=tiff.imread('FondoNegro-1.tif')
plt.imshow(arr/2**16)
plt.show()	
