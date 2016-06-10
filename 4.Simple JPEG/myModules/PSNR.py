import numpy as np

def PSNR(orig,approximation):
	MSE=np.square(orig-approximation).mean()
	B=orig.dtype.itemsize*8
	MAX_I=2**B-1
	return 10*np.log10(MAX_I**2/MSE),MSE
