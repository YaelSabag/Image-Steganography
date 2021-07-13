# Image Steganography Based on Local Variance
The system implements stenography in images.

## Table of Content
* [General Information](#general-information)
* [Technologies](#technologies)
* [Setup](#setup)
* [Team](#team)

## General Information 
The system encrypts a message within an image and producing an image with a watermark.
In addition, the system implements the extraction and decoding of the encrypted message from the image.

We added 3 improvements to the system:
1. You can select color images and encrypt them.
2. You can also add a layer of protection and encrypt the message and then hide the encrypted message in the image so that after extracting from the image it is necessary to    decrypt it in order to receive the original message.
3. Lastly, the system also works with images with white noise.

## Technologies
The system runs on a Windows operating system and is built with Visual Studio Code and created with:
*Python version :3.8.3
*numpy
*tkinter
*PIL


## Setup
Clone this repo to your desktop and run: 

 `pip install numpy`

 `pip install PIL`
 
 `pip install tk`
 
 `pip install Pillow`
 
 ## Team
 * Hodaya Siman Tov
 * Kineret Levi
 * Yael Sabag
 * Shaked Levi
 * Rachel Levi
