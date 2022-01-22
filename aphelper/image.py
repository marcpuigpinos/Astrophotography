from astropy.io import fits
import numpy as np
from PIL import Image
from math import pow

def normalize(data, bits):
    data = data / np.max(data)
    data = (pow(2, bits[0])-1) * data
    return data.astype(bits[1])

def set_brightness(data, brightness, bits):
    if brightness < 0:
        brightness = 0
    data = data * brightness
    return data.astype(bits[1])

def mirrorH(data, resx, resy):
    data_aux = data
    for i in range(resx):
        for j in range(int(resy/2)):
            data[i,j] = data_aux[i,resy-1-j]
        for j in range(int(resy/2)):
            data[i,resy-1-j] = data_aux[i,j]
    return data

class fits_image:
    def __init__(self, file_name):
        hdulist = fits.open(file_name)
        if len(hdulist[0].data.shape) == 3:
            self.__layers = hdulist[0].data.shape[0]
            self.__resx = hdulist[0].data.shape[2]
            self.__resy = hdulist[0].data.shape[1]
        else:
            self.__layers = 1
            self.__resx = hdulist[0].data.shape[1]
            self.__resy = hdulist[0].data.shape[0]            
        self.__data = hdulist[0].data[0,:,:].T
        self.__red = None
        self.__green = None
        self.__blue = None
        if self.__layers == 3:
            self.__red = hdulist[0].data[0,:,:].T
            self.__green = hdulist[0].data[1,:,:].T
            self.__blue = hdulist[0].data[2,:,:].T
        
    def info(self):
        print("Number of layers: ", self.__layers)
        print("Resolution: ", self.__resx, "x", self.__resy)

    def save(self, file_name, color_bits=None, brightness=None):
        if color_bits == None or color_bits == 8:
            bits = (8, np.uint8)
        elif color_bits == 16:
            bits = (16, np.uint16)
        elif color_bits == 32:
            bits = (32, np.uint32)
        else:
            bits = (8, np.uint8)

        if brightness == None:
            brightness = 1
        
        if self.__layers == 3:
            self.__red = normalize(self.__red, bits)
            self.__green = normalize(self.__green, bits)
            self.__blue = normalize(self.__blue, bits)
            self.__red = set_brightness(self.__red, brightness, bits)
            self.__green = set_brightness(self.__green, brightness, bits)
            self.__blue = set_brightness(self.__blue, brightness, bits)
            red = Image.fromarray(self.__red)
            green = Image.fromarray(self.__green)
            blue = Image.fromarray(self.__blue)
            rgb = Image.merge("RGB",(red,green,blue))
            rgb.save(file_name)
        else:
            self.__data = set_brightness(self.__data, brightness)
            self.__data = normalize(self.__data, bits)
            img = Image.fromarray(self.__data)
            img = img.convert('RGB')
            img.save(file_name)

    def rotate90(self):
        self.__data = np.rot90(self.__data)
        if self.__layers == 3:
            self.__red = np.rot90(self.__red)
            self.__green = np.rot90(self.__green)
            self.__blue = np.rot90(self.__blue)
        resx = self.__resx
        self.__resx = self.__resy
        self.__resy = resx

    def __mirrorH(self):
        self.__data = mirrorH(self.__data, self.__resx, self.__resy)
        if self.__layers == 3:
            self.__red = mirrorH(self.__red, self.__resx, self.__resy)
            self.__green = mirrorH(self.__green, self.__resx, self.__resy)
            self.__blue = mirrorH(self.__blue, self.__resx, self.__resy)
        

        

        


