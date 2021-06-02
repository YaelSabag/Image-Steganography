# import cv2

# img = cv2.imread('images/garayScaleImg.jpg',2)
# ret, bw_img = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
# cv2.imshow("Binary Image",bw_img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

import numpy as np
from PIL import Image
import random
import cv2
import textwrap

def getIndex(height,width,pixelLocation,mat):
    indexRow=-1
    indexCol=-1
    for i in range(height):
        for j in range(width):
            if(mat[i][j]==pixelLocation):
                indexRow=i
                indexCol=j
                break
    return indexRow,indexCol
def checkLocationPixel(pixelLocation,width,height,mat,arrPixel):
    indexRow,indexCol=getIndex(height,width,pixelLocation,mat)
    if(indexRow==0 or indexRow==(height-1) or indexCol==0 or indexCol==(width-1)):
        return False
    if((mat[indexRow-1][indexCol] in arrPixel) or (mat[indexRow+1][indexCol] in arrPixel)or (mat[indexRow][indexCol-1] in arrPixel) or (mat[indexRow][indexCol+1] in arrPixel)or (mat[indexRow-1][indexCol-1] in arrPixel)or (mat[indexRow-1][indexCol+1] in arrPixel)or(mat[indexRow+1][indexCol-1] in arrPixel) or (mat[indexRow+1][indexCol+1] in arrPixel) ):
        return False
    if(mat[indexRow][indexCol] in arrPixel):
        return False
    return True
def chochePixel(width,height,num_pixel):
    count=0
    mat=[]
    for i in range(height):
        arr=[]
        for j in range(width):
            arr.append(count)
            count=count+1
        mat.append(arr)
    hidenPixel=[]
    i=0
    while(i<num_pixel):
        x=random.randint(0,(width*height)-1)
        if(checkLocationPixel(x,width,height,mat,hidenPixel)==True):
            hidenPixel.append(x)
            i=i+1
    hidenPixel.sort()
    return  hidenPixel, mat
def getMedPixels(hidenPixel,mat,arrPixel,width,height):
    med=[]
    medPixel=0
    for i in range(len(hidenPixel)):
        indexRow,indexCol = getIndex(height,width,hidenPixel[i],mat)
        indexRow=int(indexRow)
        indexCol=int(indexCol)
        medPixel = int(arrPixel[indexRow-1][indexCol-1])+int(arrPixel[indexRow-1][indexCol])+int(arrPixel[indexRow-1][indexCol+1])+int(arrPixel[indexRow][indexCol-1])+int(arrPixel[indexRow][indexCol+1])+int(arrPixel[indexRow+1][indexCol-1])+int(arrPixel[indexRow+1][indexCol])+int(arrPixel[indexRow+1][indexCol+1])
        medPixel=medPixel/8
        med.append(medPixel)
    return med
def getVarPixels(hidenPixel,mat,arrPixel,width,height,med):
    var=[]
    varPixel=0
    for i in range(len(hidenPixel)):
        indexRow,indexCol = getIndex(height,width,hidenPixel[i],mat)
        indexRow=int(indexRow)
        indexCol=int(indexCol)
        varPixel =(arrPixel[indexRow-1][indexCol-1]-med[i])**2+(arrPixel[indexRow-1][indexCol]-med[i])**2+(arrPixel[indexRow-1][indexCol+1]-med[i])**2+(arrPixel[indexRow][indexCol-1]-med[i])**2+(arrPixel[indexRow][indexCol+1]-med[i])**2+(arrPixel[indexRow+1][indexCol-1]-med[i])**2+(arrPixel[indexRow+1][indexCol]-med[i])**2+(arrPixel[indexRow+1][indexCol+1]-med[i])**2
        var.append(varPixel)
    return var

def Encode(src, message, dest):

    img = Image.open(src, 'r')
    
    # width, height = img.size
    img1 = Image.open(src, 'r').convert('LA')
    img1.save('greyscale.png')
    img2 = cv2.imread('greyscale.png', 0) 
    height,width=img2.shape[0],img2.shape[1]
    
    # for i in range (img2.shape[0]): #traverses through height of the image
    #     for j in range (img2.shape[1]): #traverses through width of the image
    #         print(img2[i][j])



    # arr1=np.array(list(img1.getdata()))
    # print(arr1)
    
    # array = np.array(img.getdata())
    # print(array)
    # n=2
    # if img.mode == 'RGB':
    #     n = 3
    # elif img.mode == 'RGBA':
    #     n = 4
    total_pixels = img2.size
    message += "$t3g0"
    b_message = ''.join([format(ord(i), "08b") for i in message])
    req_pixels = len(b_message)
    if req_pixels > total_pixels:
        print("ERROR: Need larger file size")
    else:
        hidenPixel,mat=chochePixel(width,height,len(b_message))
        med=getMedPixels(hidenPixel,mat,img2,width,height)
        var=getVarPixels(hidenPixel,mat,img2,width,height,med)
        maxVar=max(var)
        division =6
        step =maxVar/division
        # b_message=textwrap.wrap(b_message, 2)
        # print(step)
        # t=(width*height)/step 
        # print(t)
        index=0
        for i in range(len(hidenPixel)):
            indexRow,indexCol = getIndex(height,width,hidenPixel[i],mat)
            img2[indexRow][indexCol] = int(bin(img2[indexRow][indexCol])+b_message[index],2)
            index=index+1
        img2=img2.reshape(height, width,1)
        # enc_img = Image.fromarray(img2.astype('uint8'), img2.mode)
        # enc_img.save("newImage.png")
        # print("Image Encoded Successfully")
    return  hidenPixel ,mat         
    # print( total_pixels)
def Decode(src,hidenPixel,mat):
    img1 = Image.open(src, 'r').convert('LA')
    img1.save('greyscale.png')
    img2 = cv2.imread('greyscale.png', 0) 
    height,width=img2.shape[0],img2.shape[1]
    # array = np.array(list(img.getdata()))

    # if img.mode == 'RGB':
    #     n = 3
    # elif img.mode == 'RGBA':
    #     n = 4
    # Divide by n according to the RGB / RGBA format
    total_pixels = img2.size

    hidden_bits = ""
    for i in range(len(hidenPixel)):
        indexRow,indexCol = getIndex(height,width,hidenPixel[i],mat)
        hidden_bits += ((bin(img2[indexRow][indexCol]))[2:][-1])

    hidden_bits = [hidden_bits[i:i+8] for i in range(0, len(hidden_bits), 8)]
    print(hidden_bits)
    message = ""
    for i in range(len(hidden_bits)):
        if message[-5:] == "$t3g0":
            break
        else:
            message += chr(int(hidden_bits[i], 2))
    if "$t3g0" in message:
        print("Hidden Message:", message[:-5])
    else:
        print("No Hidden Message Found")


hidenPixel,mat=Encode('garayScaleImg.jpg', 'AAA', 'newGarayScaleImg.jpg')
# Decode('garayScaleImg.jpg',hidenPixel,mat)

