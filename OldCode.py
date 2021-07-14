"""
Submited By:
Hodaya Siman Tov 
Kineret Levi
Yael sabag
Shaked Levi
Rachel Levi
"""
import numpy as np
from tkinter import filedialog
from tkinter import *
import PIL.Image
from PIL import Image

WHITE  = '\033[0m'  # white (normal)
RED  = '\033[31m' # red
GREEN  = '\033[32m' # green
ORANGE  = '\033[33m' # orange
BLUE  = '\033[34m' # blue
PURPLE  = '\033[35m' # purple

def Encode(src, message, dest, qualSecu):
    preMessage = message
    fp = open(src,"rb")
    img = PIL.Image.open(fp) 
    width, height = img.size
    array = np.array(list(img.getdata()))
    if img.mode == 'RGB':
        n = 3
    elif img.mode == 'RGBA':
        n = 4
    totalPixels = array.size//n
    message += "$t3g0"
    encryptedMessage = ''.join([format(ord(i), "08b") for i in message])
    reqPixels = len(encryptedMessage)

    if reqPixels > totalPixels:
        print(RED+"ERROR: Message to big  for file"+WHITE)

    else:
        index = 0
        for p in range(totalPixels):
            for q in range(0, 3):
                if index < reqPixels:
                    if qualSecu == '1':
                        array[p][q] = int(bin(array[p][q])[7:9] + encryptedMessage[index], 2)
                        index += 1
                    elif qualSecu == '2':
                        array[p][q] = int(bin(array[p][q])[5:7] + encryptedMessage[index], 2)
                        index += 1
                    elif qualSecu == '3':
                        array[p][q] = int(bin(array[p][q])[6:8] + encryptedMessage[index], 2)
                        index += 1

        array = array.reshape(height, width, n)
        encImg = Image.fromarray(array.astype('uint8'), img.mode)
        encImg.save(dest)
        if checkEncryption(preMessage,dest):
            print("The Stegnographed image is as shown below: ")
            encImg.show()
            print(ORANGE+"Image Encoded Successfully"+WHITE)
        else:
            print(RED+"ERROR: Input is wrong"+WHITE)
            exit(1)


def checkEncryption(preMessage,src):
    img = Image.open(src,'r')
    array = np.array(list(img.getdata()))
    if img.mode == 'RGB':
        n = 3
    elif img.mode == 'RGBA':
        n = 4
    # Divide by n according to the RGB / RGBA format
    totalPixels = array.size // n
    hiddenBits = ""
    for p in range(totalPixels):
        for q in range(0, 3):
            hiddenBits += (bin(array[p][q])[2:][-1])

    hiddenBits = [hiddenBits[i:i + 8] for i in range(0, len(hiddenBits), 8)]
    message = ""
    for i in range(len(hiddenBits)):
        if message[-5:] == "$t3g0":
            break
        else:
            message += chr(int(hiddenBits[i], 2))
    if "$t3g0" in message:
        message = message[:-5]
        if preMessage == message:
            return True
    else:
        return False


def Decode(src):
    fp = open(src,"rb")
    img = PIL.Image.open(fp)
    array = np.array(list(img.getdata()))

    if img.mode == 'RGB':
        n = 3
    elif img.mode == 'RGBA':
        n = 4
    totalPixels = array.size//n

    hiddenBits = ""
    for p in range(totalPixels):
        for q in range(0, 3):
            hiddenBits += (bin(array[p][q])[2:][-1])

    hiddenBits = [hiddenBits[i:i+8] for i in range(0, len(hiddenBits), 8)]

    message = ""
    for i in range(len(hiddenBits)):
        if message[-5:] == "$t3g0":
            break
        else:
            message += chr(int(hiddenBits[i], 2))
    if "$t3g0" in message:
        print(PURPLE+"Hidden message:"+WHITE, message[:-5])
    else:
        print(RED+"No message has found"+WHITE)


if __name__ == "__main__":
    
    userInput = input(PURPLE+"\n----------Image Steganography----------\n{0}1.{1} Encode the data \n{0}2.{1} Decode the data \nPlease enter input : ".format(PURPLE,WHITE))
    root = Tk()
    if userInput == '1':
        qualSecu = input("\n{0}Please choose one option:\n1.{1} High quality.\n{0}2.{1} High security.\n{0}3.{1} Average quality and security.\n".format(PURPLE,WHITE))
        if qualSecu != '1' and qualSecu != '2' and qualSecu != '3':
            print(RED+"ERROR: Input is wrong"+WHITE)
            exit(1)
        root.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("jpeg files","*.jpeg"),("jpeg files","*.png"),("all files","*.*")))
        # print (root.filename) #returns file path
        src =root.filename
        message = input(PURPLE+"Please enter message to encrypt: "+WHITE)
        fileName= input(PURPLE+"Please enter the name of new encoded image(without extension): "+WHITE)
        fileName+=".png"
        print(ORANGE+"Encoding...."+WHITE)
        Encode(src, message,fileName, qualSecu)

    elif userInput == '2':
        root.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("jpeg files","*.jpeg"),("jpeg files","*.png"),("all files","*.*")))
        imageName=root.filename
        print(ORANGE+"Decoding...."+WHITE)
        Decode(imageName)

    else:
        print(RED+"ERROR: Input is wrong"+WHITE)
        exit(1)