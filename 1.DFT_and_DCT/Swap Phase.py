#! /usr/bin/python3

if __name__=="__main__":

    from PIL import Image
    import numpy as np
    from matplotlib import pyplot as plt
    from scipy.fftpack import dct
    from scipy.fftpack import idct

    #
    default_paths=["img1.jpg","img2.jpg"]
    paths=[None]*2
    images=[None]*2
    DFT=[None]*2
    iDFT=[None]*2
    Magnitude=[None]*2
    phase=[None]*2
    for i in range(2):
        while True:
            paths[i]=input("Path to the image: (default to "+default_paths[i]+") ")
            if paths[i] is "":
                paths[i]=default_paths[i]
            try:
                images[i]=Image.open(paths[i])
                break
            except FileNotFoundError as e:
                print(e)
                print("Try again.")
        #Image processing
        #Get grayscale
        images[i]=images[i].convert('L')
        #Find DFT
        DFT[i]=np.fft.fft2(images[i])
        Magnitude[i]=abs(DFT[i])
        phase[i]=DFT[i]/Magnitude[i]

    #Swap the phases of these two images
    iDFT[0]=abs(np.fft.ifft2(Magnitude[0]*phase[1]))
    iDFT[1]=abs(np.fft.ifft2(Magnitude[1]*phase[0]))
    #Show results
	#The 'interpolation="none"' makes pyplot display the image pixel by pixel
    plt.subplot(221),plt.imshow(images[0], cmap = 'gray',interpolation="none")
    plt.title('Original Image#1'), plt.xticks([]), plt.yticks([])
    plt.subplot(222),plt.imshow(images[1], cmap = 'gray',interpolation="none")
    plt.title('Original Image#2'), plt.xticks([]), plt.yticks([])
    plt.subplot(223),plt.imshow(iDFT[0], cmap = 'gray',interpolation="none")
    plt.title('Magnitude#1 + Phase#2'), plt.xticks([]), plt.yticks([])
    plt.subplot(224),plt.imshow(iDFT[1], cmap = 'gray',interpolation="none")
    plt.title('Magnitude#2 + Phase#1'), plt.xticks([]), plt.yticks([])
    plt.show()
