#! /usr/bin/python3

if __name__=="__main__":

    from PIL import Image
    import numpy as np
    from matplotlib import pyplot as plt
    from scipy.fftpack import dct
    from scipy.fftpack import idct
    
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
    DFT=np.fft.fft2(image)
    iDFT=abs(np.fft.ifft2(DFT))
    DFT=np.fft.fftshift(DFT)
    M=np.maximum(20*np.log(abs(DFT)),1e-100)
    #Find DCT
    DCT=dct(dct(image,norm="ortho").T,norm="ortho").T
    iDCT=idct(idct(DCT,norm="ortho").T,norm="ortho").T
    N=np.maximum(20*np.log(abs(DCT)),1e-100)
    

    #Show results
	#The 'interpolation="none"' makes pyplot display the image pixel by pixel
    plt.subplot(421),plt.imshow(image, cmap = 'gray',interpolation="none")
    plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(422),plt.imshow(M, cmap = 'gray',interpolation="none")
    plt.title('Magnitude Spectrum (DFT)'), plt.xticks([]), plt.yticks([])
    plt.subplot(423),plt.imshow(iDFT, cmap = 'gray',interpolation="none")
    plt.title('Inverse Transformation (iDFT)'), plt.xticks([]), plt.yticks([])
    plt.subplot(425),plt.imshow(image, cmap = 'gray',interpolation="none")
    plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(426),plt.imshow(N, cmap = 'gray',interpolation="none")
    plt.title('Magnitude Spectrum (DCT)'), plt.xticks([]), plt.yticks([])
    plt.subplot(427),plt.imshow(iDCT, cmap = 'gray',interpolation="none")
    plt.title('Inverse Transformation (iDCT)'), plt.xticks([]), plt.yticks([])
    plt.show()
