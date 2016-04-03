#! /usr/bin/python3

if __name__=="__main__":

    from PIL import Image
    import numpy as np
    from matplotlib import pyplot as plt
    from scipy.fftpack import dct
    from scipy.fftpack import idct
    import math

    def my_fft2(x):
        w,h=image.size
        U=np.matrix(np.zeros((h,h),complex))
        V=np.matrix(np.zeros((w,w),complex))
        for i in range(h):
            for j in range(h):
                U[i,j]=np.exp(-1j*2*math.pi*i*j/h)
        for i in range(w):
            for j in range(w):
                V[i,j]=np.exp(-1j*2*math.pi*i*j/w)
        return np.array(U*np.matrix(image)*V)/math.sqrt(w*h)
    #
    default_path="img1.jpg"
    path=""
    image=None
    while True:
        path=input("Path to the image: (default to "+default_path+") ")
        if path is "":
            path=default_path
        try:
            image=Image.open(path)
            break
        except FileNotFoundError as e:
            print(e)
            print("Try again.")

    #Image processing
    #Get grayscale
    image=image.convert('L')
    #Find DFT
    DFT=my_fft2(image)
    iDFT=abs(np.fft.ifft2(DFT))
    DFT=np.fft.fftshift(DFT)
    M=20*np.log(abs(DFT))
    #Find DCT
    DCT=dct(dct(image,norm="ortho").T,norm="ortho").T
    iDCT=idct(idct(DCT,norm="ortho").T,norm="ortho").T
    N=20*np.log(abs(DCT))
    

    #Show results
	#The 'interpolation="none"' makes pyplot display the image pixel by pixel
    plt.subplot(421),plt.imshow(image, cmap = 'gray',interpolation="none")
    plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(422),plt.imshow(np.maximum(M,-200), cmap = 'gray',interpolation="none")
    plt.title('Magnitude Spectrum (DFT)'), plt.xticks([]), plt.yticks([])
    plt.subplot(423),plt.imshow(iDFT, cmap = 'gray',interpolation="none")
    plt.title('Inverse Transformation (iDFT)'), plt.xticks([]), plt.yticks([])
    plt.subplot(425),plt.imshow(image, cmap = 'gray',interpolation="none")
    plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(426),plt.imshow(np.maximum(N,-200), cmap = 'gray',interpolation="none")
    plt.title('Magnitude Spectrum (DCT)'), plt.xticks([]), plt.yticks([])
    plt.subplot(427),plt.imshow(iDCT, cmap = 'gray',interpolation="none")
    plt.title('Inverse Transformation (iDCT)'), plt.xticks([]), plt.yticks([])
    plt.show()
