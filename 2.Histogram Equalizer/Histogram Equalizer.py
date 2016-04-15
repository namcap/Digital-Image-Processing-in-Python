#! /usr/bin/python3

if __name__=="__main__":

    from PIL import Image
    import numpy as np
    from matplotlib import pyplot as plt

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
    w,h=image.size
    #Convert to numpy array
    image=np.array(image)
    p=np.zeros(256) #contains number of occurrence of each intensity level
    for i in range(h):
    	for j in range(w):
    		p[image[i,j]]+=1
    T=np.zeros(256) #Intensity mapping
    accumlator=0
    for i in range(256):
    	accumlator+=p[i]
    	T[i]=accumlator
    T=np.round(255*T/(h*w))
    output=np.zeros((h,w)) #Image processed
    for i in range(h):
    	for j in range(w):
    		output[i,j]=T[image[i,j]] #Apply the intensity mapping

   	#Show results
    plt.subplot(221),plt.imshow(image, cmap = 'gray',interpolation="none")
    plt.title('Original image #1'), plt.xticks([]), plt.yticks([])
    plt.subplot(222),plt.hist(image.ravel(),bins=256,range=(0,255))
    plt.title('Histogram of #1'),plt.xlim(0,255)
    plt.subplot(223),plt.imshow(output, cmap = 'gray',interpolation="none")
    plt.title('Image after processing #2'), plt.xticks([]), plt.yticks([])
    plt.subplot(224),plt.hist(output.ravel(),bins=256,range=(0,255))
    plt.title('Histogram of #2'),plt.xlim(0,255)
    plt.show()
