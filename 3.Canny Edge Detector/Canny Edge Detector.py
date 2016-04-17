#! /usr/bin/python3

def main():

    global my_stack,image,w,h,smoothed,gradient,M,M1
    class my_stack:

        def __init__(self,size=1,max_size=-1):
            self.__size=size if 0<size else 1
            self.__max_size=max_size
            self.__index=0
            self.__data=[None]*self.__size

        def __double_size(self):
            if 0<self.__max_size<2*self.__size:
                self.__data+=[None]*(self.__max_size-self.__size)
                self.__size=self.__max_size
            else:
                self.__data+=[None]*self.__size
                self.__size*=2

        def push(self,ele):
            if (self.__size-1<self.__index):
                self.__double_size()
            try:
                self.__data[self.__index]=ele #will throw an exception if __double_size() fails
            except:
                raise
            self.__index+=1

        def pop(self):
            if (0<self.__index):
                self.__index-=1
                return self.__data[self.__index]
            else:
                return None

        def is_empty(self):
            return self.__index==0


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

    #Smooth the image to reduce the magnitude of noise
    smoothed=gaussian_filter(image,sigma=1.4)

    #Find gradient
    kx=np.array([  [-1,0,1],
                    [-2,0,2],
                    [-1,0,1]])
    ky=np.array([  [1,2,1],
                    [0,0,0],
                    [-1,-2,-1]])*1j
    gradient=convolve2d(image,kx,mode='same')+convolve2d(image,ky,mode='same')

    #Apply none-maximum suppression
    M=abs(gradient) #gradient magnitude
    angle=np.angle(gradient)*180/np.pi
    M1=np.zeros((h,w))
    t=0
    for i in range(1,h-1):
        for j in range(1,w-1):
            if M[i][j]==0:
                continue
            if 0<angle[i][j]:
                if angle[i][j]<=45:
                    t=gradient[i][j].imag/gradient[i][j].real
                    #Intepolation
                    if t*M[i-1][j+1]+(1-t)*M[i][j+1]<=M[i][j] and t*M[i+1][j-1]+(1-t)*M[i][j-1]<=M[i][j]:
                        M1[i][j]=M[i][j]
                elif angle[i][j]<=90:
                    t=gradient[i][j].real/gradient[i][j].imag
                    #Intepolation
                    if t*M[i-1][j+1]+(1-t)*M[i-1][j]<=M[i][j] and t*M[i+1][j-1]+(1-t)*M[i+1][j]<=M[i][j]:
                        M1[i][j]=M[i][j]
                elif angle[i][j]<=135:
                    t=-gradient[i][j].real/gradient[i][j].imag
                    #Intepolation
                    if t*M[i-1][j-1]+(1-t)*M[i-1][j]<=M[i][j] and t*M[i+1][j+1]+(1-t)*M[i+1][j]<=M[i][j]:
                        M1[i][j]=M[i][j]
                else:
                    t=-gradient[i][j].imag/gradient[i][j].real
                    #Intepolation
                    if t*M[i-1][j-1]+(1-t)*M[i][j-1]<=M[i][j] and t*M[i+1][j+1]+(1-t)*M[i][j+1]<=M[i][j]:
                        M1[i][j]=M[i][j]
            else:
                if -45<angle[i][j]:
                    t=-gradient[i][j].imag/gradient[i][j].real
                    #Intepolation
                    if t*M[i-1][j-1]+(1-t)*M[i][j-1]<=M[i][j] and t*M[i+1][j+1]+(1-t)*M[i][j+1]<=M[i][j]:
                        M1[i][j]=M[i][j]
                elif -90<angle[i][j]:
                    t=-gradient[i][j].real/gradient[i][j].imag
                    #Intepolation
                    if t*M[i-1][j-1]+(1-t)*M[i-1][j]<=M[i][j] and t*M[i+1][j+1]+(1-t)*M[i+1][j]<=M[i][j]:
                        M1[i][j]=M[i][j]
                elif -135<angle[i][j]:
                    t=gradient[i][j].real/gradient[i][j].imag
                    #Intepolation
                    if t*M[i-1][j+1]+(1-t)*M[i-1][j]<=M[i][j] and t*M[i+1][j-1]+(1-t)*M[i+1][j]<=M[i][j]:
                        M1[i][j]=M[i][j]
                else:
                    t=gradient[i][j].imag/gradient[i][j].real
                    #Intepolation
                    if t*M[i-1][j+1]+(1-t)*M[i][j+1]<=M[i][j] and t*M[i+1][j-1]+(1-t)*M[i][j-1]<=M[i][j]:
                        M1[i][j]=M[i][j]

    cal(init_VH,init_VL) #Double threshold and Edge tracking

def cal(VH,VL):
    #Double threshold
    global M1,strong,weak,output,stack
    strong=VH<=M1
    weak=(VL<=M1)*(M1<VH)

    #Edge tracking
    temp=np.array(weak)
    output=np.array(strong)
    try:
        stack
    except NameError:
        stack=my_stack(size=temp.sum(),max_size=w*h)
    for i in range(1,h):
        for j in range(1,w):
            if output[i][j]:
                for l in [(i-1,j-1),(i,j-1),(i+1,j-1),(i+1,j),(i+1,j+1),(i,j+1),(i-1,j+1),(i-1,j)]:
                    try:
                        weak[l]
                    except IndexError:
                        continue
                    if weak[l]:
                        output[l]=True
                        weak[l]=False
                        stack.push(l)
    while not stack.is_empty():
        l=stack.pop()
        i=l[0]
        j=l[1]
        for l in [(i-1,j-1),(i,j-1),(i+1,j-1),(i+1,j),(i+1,j+1),(i,j+1),(i-1,j+1),(i-1,j)]:
            try:
                weak[l]
            except IndexError:
                continue
            if weak[l]:
                output[l]=True
                weak[l]=False
                stack.push(l)

def redraw():
    im5.set_data(strong*180+weak*60)
    im6.set_data(np.concatenate((strong[:,:,None],output[:,:,None],(weak*(-output)+strong)[:,:,None]),axis=2))
    im7.set_data(output)

def update_results(val):
    cal(Slider_VH.val,Slider_VL.val)
    redraw()

if __name__=="__main__":
    from PIL import Image
    import numpy as np
    from matplotlib import pyplot as plt
    from scipy.ndimage.filters import gaussian_filter
    from scipy.signal import convolve2d
    from matplotlib.widgets import Slider

    plt.subplots_adjust(bottom=0.25)
    axVH=plt.axes([0.25, 0.1, 0.65, 0.03])
    axVL=plt.axes([0.25, 0.15, 0.65, 0.03])
    init_VH,init_VL=0,0
    Slider_VH=Slider(axVH,'High threshold',0,1000,valinit=init_VH)
    Slider_VH.on_changed(update_results)
    Slider_VL=Slider(axVL,'Low threshold',0,1000,valinit=init_VL)
    Slider_VL.on_changed(update_results)
    main()
    #Show results
    plt.subplot(241),plt.imshow(image, cmap = 'gray',interpolation="none")
    plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(242),plt.imshow(smoothed, cmap = 'gray',interpolation="none")
    plt.title('Smoothed'), plt.xticks([]), plt.yticks([])
    plt.subplot(243),plt.imshow(M, cmap = 'gray',interpolation="none")
    plt.title('Gradient Magnitude'), plt.xticks([]), plt.yticks([])
    plt.subplot(244),plt.imshow(M1, cmap = 'gray',interpolation="none")
    plt.title('After Non-maximium Suppression'), plt.xticks([]), plt.yticks([])
    plt.subplot(245)
    im5=plt.imshow(strong*255+weak*75, cmap = 'gray',vmin=0,vmax=255,interpolation="none")
    plt.title('Double Threshold\n(Strong edges in white and weak ones in grey)'), plt.xticks([]), plt.yticks([])
    plt.subplot(246)
    im6=plt.imshow(np.concatenate((strong[:,:,None],output[:,:,None],(weak*(-output)+strong)[:,:,None]),axis=2), interpolation="none",vmin=0,vmax=1)
    plt.title('Edge Tracking\n(Strong edges in white,\nweak edges connected to strong edges in green\nand other weak edges in blue)'), plt.xticks([]), plt.yticks([])
    plt.subplot(247)
    im7=plt.imshow(output, cmap = 'gray',vmin=0,vmax=1,interpolation="none")
    plt.title('Output'), plt.xticks([]), plt.yticks([])
    plt.show()
