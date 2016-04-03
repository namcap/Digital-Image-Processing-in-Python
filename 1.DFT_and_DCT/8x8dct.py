#! /usr/bin/python3

if __name__=="__main__":

    from PIL import Image
    import numpy as np
    from matplotlib import pyplot as plt
    from scipy.fftpack import dct
    from scipy.fftpack import idct

    #DCT 2D
    def dct2(x):
        return dct(dct(x,norm="ortho").T,norm="ortho").T

    #iDCT 2D
    def idct2(x):
        return abs(idct(idct(x,norm="ortho").T,norm="ortho").T)
    
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
    #Crop the image so that its height and width are multiples of 8
    w,h=(np.array(image.size)/8).astype(int)*8
    image=np.array(image)[:h,:w]
    #Find DCT and extract low-frequency components
    DCT=np.zeros((h,w))
    DCT_L=np.zeros((h,w))
    iDCT=np.zeros((h,w))
    mask=np.array([
        [1,1,1,1,1,1,0,0],
        [1,1,1,1,1,0,0,0],
        [1,1,1,1,0,0,0,0],
        [1,1,1,0,0,0,0,0],
        [1,1,0,0,0,0,0,0],
        [1,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0]])
    for i in range(0,h,8):
        for j in range(0,w,8):
            #Find DCT
            DCT[i:i+8,j:j+8]=dct2(image[i:i+8,j:j+8])
            #Extract low-frequency components
            DCT_L[i:i+8,j:j+8]=DCT[i:i+8,j:j+8]*mask
            iDCT[i:i+8,j:j+8]=idct2(DCT_L[i:i+8,j:j+8])
    M=20*np.log(abs(DCT))
    N=20*np.log(abs(DCT_L))
    
    #Show results
	#The 'interpolation="none"' makes pyplot display the image pixel by pixel
    plt.subplot(221),plt.imshow(image, cmap = 'gray',interpolation="none")
    plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(222),plt.imshow(np.maximum(M,-200), cmap = 'gray',interpolation="none")
    plt.title('Magnitude Spectrum (8x8 DCT)'), plt.xticks([]), plt.yticks([])
    plt.subplot(223),plt.imshow(iDCT, cmap = 'gray',interpolation="none")
    plt.title('Inverse Transformation (8x8 DCT)'), plt.xticks([]), plt.yticks([])
    plt.subplot(224),plt.imshow(np.maximum(N,-200), cmap = 'gray',interpolation="none")
    plt.title('Magnitude Spectrum (8x8 DCT)\nLow-frequency components'), plt.xticks([]), plt.yticks([])
    plt.show()
