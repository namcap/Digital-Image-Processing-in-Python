from scipy.fftpack import dct
from scipy.fftpack import idct

#DCT 2D
def dct2(x):
    return dct(dct(x,norm="ortho").T,norm="ortho").T

#iDCT 2D
def idct2(x):
    return idct(idct(x,norm="ortho").T,norm="ortho").T
