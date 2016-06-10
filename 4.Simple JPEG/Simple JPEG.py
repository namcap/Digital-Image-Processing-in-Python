#! /usr/bin/python3
#This program performs simple JPEG compression (no Huffman coding) with
#different quantization tables, determines quality of the compressed image
#by computing PSNR and generates PSNR-size curve to see
#the impact of compression rate on image's quality

from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
from myModules import JPEG
from myModules import PSNR

#JPEG quantization tables
NO_COMPRESSION=np.array([
    [1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1]])
LOW_COMPRESSION=np.array([
    [1,1,1,1,1,2,2,4],
    [1,1,1,1,1,2,2,4],
    [1,1,1,1,2,2,2,4],
    [1,1,1,1,2,2,4,8],
    [1,1,2,2,2,2,4,8],
    [2,2,2,2,2,4,8,8],
    [2,2,2,4,4,8,8,16],
    [4,4,4,4,8,8,16,16]])
HIGH_COMPRESSION=np.array([
    [1,2,4,8,16,32,64,128],
    [2,4,4,8,16,32,64,128],
    [4,4,8,16,32,64,128,128],
    [8,8,16,32,64,128,128,256],
    [16,16,32,64,128,128,256,256],
    [32,32,64,128,128,256,256,256],
    [64,64,128,128,256,256,256,256],
    [128,128,128,256,256,256,256,256]])

if __name__=="__main__":
    #Deal with user input
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
    #Crop the image so that its height and width are multiples of 8
    w,h=(np.array(image.size)/8).astype(int)*8
    image=np.array(image)[:h,:w]
    #Store results
    sorted_results=[]
    #Low compression
    RLE=JPEG.compress(image,low_compression=NO_COMPRESSION,high_compression=LOW_COMPRESSION)
    RGB=JPEG.decompress(RLE,size=image.shape,low_compression=NO_COMPRESSION,high_compression=LOW_COMPRESSION)
    sorted_results.append({'RLE':RLE,'RGB':RGB,'name':'Low Compression'})
    #Medium compression
    RLE=JPEG.compress(image,low_compression=LOW_COMPRESSION,high_compression=HIGH_COMPRESSION)
    RGB=JPEG.decompress(RLE,size=image.shape,low_compression=LOW_COMPRESSION,high_compression=HIGH_COMPRESSION)
    sorted_results.append({'RLE':RLE,'RGB':RGB,'name':'Medium Compression'})
    #High compression
    RLE=JPEG.compress(image,low_compression=HIGH_COMPRESSION,high_compression=HIGH_COMPRESSION)
    RGB=JPEG.decompress(RLE,size=image.shape,low_compression=HIGH_COMPRESSION,high_compression=HIGH_COMPRESSION)
    sorted_results.append({'RLE':RLE,'RGB':RGB,'name':'High Compression'})
    #Other tests # (low_compression, high_compression) pairs
    tests=[(LOW_COMPRESSION,LOW_COMPRESSION),(NO_COMPRESSION,NO_COMPRESSION)]
    for i in tests:
        RLE=JPEG.compress(image,low_compression=i[0],high_compression=i[1])
        RGB=JPEG.decompress(RLE,size=image.shape,low_compression=i[0],high_compression=i[1])
        sorted_results.append({'RLE':RLE,'RGB':RGB})

    #Compute size after compression and PSNR
    for i in sorted_results:
        i['num_fields']=len(i['RLE'][0])+len(i['RLE'][1])+len(i['RLE'][2])
        i['PSNR']=PSNR.PSNR(image,i['RGB'])[0]
    results=sorted_results[0:3]
    #Sort the results by size 'num_fields'
    sorted_results.sort(key=lambda x: x['num_fields'])

    #Save results to files
    for i in results:
        Image.fromarray(i['RGB']).save(i['name'].replace(' ','_')+'.bmp')

    #Show results
    plt.figure(1),plt.imshow(image, interpolation="none")
    plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    plt.figure(2),plt.imshow(results[0]['RGB'], interpolation="none")
    plt.title(results[0]['name']), plt.xticks([]), plt.yticks([])
    plt.figure(3),plt.imshow(results[1]['RGB'], interpolation="none")
    plt.title(results[1]['name']), plt.xticks([]), plt.yticks([])
    plt.figure(4),plt.imshow(results[2]['RGB'], interpolation="none")
    plt.title(results[2]['name']), plt.xticks([]), plt.yticks([])
    plt.figure(5),plt.plot([ i['num_fields'] for i in sorted_results ], [ i['PSNR'] for i in sorted_results ], marker='o')
    plt.title('PSNR vs size'), plt.xlabel('size'), plt.ylabel('PSNR (dB)')
    plt.plot([ i['num_fields'] for i in results ], [ i['PSNR'] for i in results ], color='m', linestyle='None', marker='o')
    for i in results:
        plt.annotate(i['name'],
            xy=(i['num_fields'], i['PSNR']),
            horizontalalignment='left', verticalalignment='buttom')
    plt.savefig('PSNR-size_curve.png',bbox_inches='tight')
    plt.show()
