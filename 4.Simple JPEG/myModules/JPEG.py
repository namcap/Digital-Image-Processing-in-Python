import numpy as np
from myModules.dct2pack import dct2,idct2

def compress(image,low_compression,high_compression): 
    #Image processing
    ###Compression
    #Convert from RGB to YUV color space
    h,w,_=image.shape
    YUV=np.zeros((h,w,3))
    YUV[:,:,0]=image[:,:,0]*0.299+image[:,:,1]*0.587+image[:,:,2]*0.114
    YUV[:,:,1]=image[:,:,0]*(-0.14713)+image[:,:,1]*(-0.28886)+image[:,:,2]*0.436
    YUV[:,:,2]=image[:,:,0]*0.615+image[:,:,1]*(-0.51499)+image[:,:,2]*(-0.10001)
    #Find DCT for each 8x8 block
    DCT_YUV=np.zeros((h,w,3))
    for i in range(0,h,8):
        for j in range(0,w,8):
            #Find DCT
            #Y(brightness) is dominant in determining the quality of visual effect so use low_compression here
            DCT_YUV[i:i+8,j:j+8,0]=np.round(dct2(YUV[i:i+8,j:j+8,0])/low_compression).astype(int)
            DCT_YUV[i:i+8,j:j+8,1]=np.round(dct2(YUV[i:i+8,j:j+8,1])/high_compression).astype(int)
            DCT_YUV[i:i+8,j:j+8,2]=np.round(dct2(YUV[i:i+8,j:j+8,2])/high_compression).astype(int)
    #RUN Length Encoding
    RLE_YUV=[[],[],[]] #[[integer,count,integer,count,...],...]
    #Zig-Zagging
    for i in range(0,h,8):
        for j in range(0,w,8):
            for c in [0,1,2]:
                ih,iw=i,j #index vertical, horizontal
                vh,vw=-1,1 #velocity vertical, horizontal
                data=DCT_YUV[i,j,c]
                cnt=0
                RLE_YUV[c].append(int(data))
                while True:
                    if DCT_YUV[ih,iw,c]==data:
                        cnt+=1
                    else:
                        RLE_YUV[c].append(cnt)
                        data=DCT_YUV[ih,iw,c]
                        RLE_YUV[c].append(int(data))
                        cnt=1
                    if ih==i+7 and iw==j+7:
                    #Traversed this 8x8 block
                        RLE_YUV[c].append(cnt)
                        break
                    if not (i<=ih+vh<i+8):
                    #Hit the upper or lower boundary
                        #Right
                        iw+=1
                        vw=-vw
                        vh=-vh
                    elif not (j<=iw+vw<j+8):
                    #Hit the left or right boundary
                        #Down
                        ih+=1
                        vw=-vw
                        vh=-vh
                    else:
                        ih+=vh
                        iw+=vw
    return RLE_YUV
    
def decompress(RLE_YUV,size,low_compression,high_compression):
    ###Decompression
    #file size (width,height), RLE_YUV and quantization tables are known beforehand
    h,w,_=size
    DCT_YUV_2=np.zeros((h,w,3))
    for c in [0,1,2]:
        RLE_ind=0
        for i in range(0,h,8):
            for j in range(0,w,8):
                ih,iw=i,j #vertical, horizontal index
                vh,vw=-1,1 #vertical, horizontal velocity
                cnt=0
                #Zig-Zagging
                while True:
                    if cnt==0:
                        data,cnt=RLE_YUV[c][RLE_ind],RLE_YUV[c][RLE_ind+1]
                        RLE_ind+=2
                    DCT_YUV_2[ih,iw,c]=data
                    cnt-=1
                    if ih==i+7 and iw==j+7:
                    #Reached the last pixel of this 8x8 block
                        break
                    if not (i<=ih+vh<i+8):
                    #Hit the upper or lower boundary
                        #Right
                        iw+=1
                        vw=-vw
                        vh=-vh
                    elif not (j<=iw+vw<j+8):
                    #Hit the left or right boundary
                        #Down
                        ih+=1
                        vw=-vw
                        vh=-vh
                    else:
                        ih+=vh
                        iw+=vw
    YUV_2=np.zeros((h,w,3))
    #iDCT
    for i in range(0,h,8):
        for j in range(0,w,8):
            YUV_2[i:i+8,j:j+8,0]=idct2(DCT_YUV_2[i:i+8,j:j+8,0]*low_compression)
            YUV_2[i:i+8,j:j+8,1]=idct2(DCT_YUV_2[i:i+8,j:j+8,1]*high_compression)
            YUV_2[i:i+8,j:j+8,2]=idct2(DCT_YUV_2[i:i+8,j:j+8,2]*high_compression)
    #Store decompressed image
    RGB=np.zeros((h,w,3))
    RGB[:,:,0]=YUV_2[:,:,0]+YUV_2[:,:,2]*1.13983
    RGB[:,:,1]=YUV_2[:,:,0]+YUV_2[:,:,1]*(-0.39465)+YUV_2[:,:,2]*(-0.58060)
    RGB[:,:,2]=YUV_2[:,:,0]+YUV_2[:,:,1]*2.03211
    #Regulate the result
    RGB=np.maximum(np.minimum(RGB,255),0).astype('uint8')

    return RGB
