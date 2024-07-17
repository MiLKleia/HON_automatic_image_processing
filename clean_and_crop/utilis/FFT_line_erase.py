import numpy as np
import math
import cv2 as cv
import os

import utilis.FFT_functions as FFT
import utilis.FFT_extract as extract_func
import utilis.clean as etal


# Constantes
kernel_blur =  1/(100) * np.array([[1,2,4,2,1], 
                                    [2,4,8,4,2], 
                                    [4,8,16,8,4],
                                    [2,4,8,4,2],
                                    [1,2,4,2,1]]) 

kernel_sharp = np.array([[0, -1, 0],[-1, 5, -1],[0,-1,0]])
ones = (1,1,1)
zeros = (0,0,0)


def line_erase_files_in_folder(path_in, path_out, resize_ratio):
    if not os.path.exists(path_out):
        os.makedirs(path_out)
        
    for root, dirs, files in os.walk(path_in, topdown=False):
        for name in files:
            #print(name)
            temp_image = cv.imread(path_in + os.sep + name)
            temp_image = cv.cvtColor(temp_image, cv.COLOR_BGR2GRAY)
            image = cv.resize(temp_image, (0, 0), fx=resize_ratio, fy=resize_ratio)
            
            out_ima = line_erase_image_using_FFT(image)
            cv.imwrite(path_out + os.sep + name, out_ima)
    return 0       



def line_erase_image_using_FFT(image):
    u, v = image.shape
    ima = cv.filter2D(image, -1, kernel_sharp)
    kernel = np.ones((2,2), np.uint8)
    ima = cv.erode(ima, kernel, iterations=1)

    padding = np.zeros((u+v, u+v))
    padding[0:u,0:v] = ima

    # FFT change of base
    dft_ima = FFT.DFT(padding)
    ima_ph = np.angle(dft_ima)
    ima_mag = np.abs(dft_ima)

    

    # filtering the small and repeteted lines
    u_filt, v_filt = ima_mag.shape
    filter_ = np.zeros((u_filt, v_filt))

    h=int(8*u_filt//11)
    w = 25
    cv.line(filter_, [u_filt//2 -h,v_filt//2], 
                      [u_filt//2 +h,v_filt//2], ones, w) 
    cv.line(filter_, [u_filt//2,v_filt//2-h], 
                      [u_filt//2,v_filt//2+h], ones, w)
    radius = 900
    cv.circle(filter_, [u_filt//2,v_filt//2], radius, zeros, -1)

    filt_ima = np.multiply(ima_mag, filter_)

    # Reconstruction
    reconstr = FFT.reconstruct(filt_ima, ima_ph)
    small_reconstr  = reconstr[0:u,0:v]
    a = np.min(small_reconstr)
    b = np.max(small_reconstr)
    if a < b:
        small_reconstr = (small_reconstr -a)/(b-a)*255
 
    
    # post-processing
    summ = image + small_reconstr
    summ[summ>255] = 255
    summ = cv.filter2D(summ, -1, kernel_blur)
    summ = cv.filter2D(summ, -1, kernel_sharp)
    a = np.min(summ)
    b = np.max(summ)
    if a < b : 
        summ = (summ -a)/(b-a)*255
    summ = not_exactly_threshold(summ, 
                np.quantile(summ, 0.01), np.quantile(summ, 0.15))
    return summ


def line_erase_image_no_FFT(image):
    u, v = image.shape
    image = cv.filter2D(image, -1, kernel_blur)
    image[image <= np.quantile(image, 0.0875)] = 0
    image[image > np.quantile(image, 0.0875)] = 255
    image = cv.filter2D(image, -1, kernel_blur)
    image = cv.filter2D(image, -1, kernel_sharp)
    return image

def apply_function(x, function, val_max):
    n = len(function)
    out = 0
    for i in range(n-2):
        out += function[i]*np.power(x,n-i-1)
    out += function[n-2]*x
    out += function[-1]
    return max(0, min(out , val_max))
    
def redo_bornes(ima):
    a = np.min(ima)
    b = np.max(ima)
    if a < b : 
        ima = (ima -a)/(b-a)*255
    return ima    
    
def not_exactly_threshold(image, min_, max_):
    image = (image-min_)/(max_-min_)*255
    image[image < 0] = 0
    image[image > 255] = 255
    return image

