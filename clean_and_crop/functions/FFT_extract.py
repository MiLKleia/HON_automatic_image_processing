import numpy as np
import math
import cv2 as cv
import os
import torch


import functions.FFT_functions as FFT
import functions.clean  as etal


kernel_blur =  1/(100) * np.array([[1,2,4,2,1], 
                                    [2,4,8,4,2], 
                                    [4,8,16,8,4],
                                    [2,4,8,4,2],
                                    [1,2,4,2,1]]) 

kernel_sharp = np.array([[0, -1, 0],[-1, 5, -1],[0,-1,0]])
ones = (1,1,1)
zeros = (0,0,0)

x = [205, 210, 215, 220, 225, 230, 235, 240, 245, 250]
y_coeff_line = [1.45, 1.35, 1.3, 1.2, 1.05, 1, 0.8, 0.4, 0.1, 0]
y_coeff_noise = [1.45, 1.35, 1.3, 1.2, 1.05, 1, 0.9, 0.85, 0.8, 0.75]
y_seuil_all = [0.92, 0.93, 0.935, 0.945, 0.955, 0.965, 0.98, 0.985, 0.995, 0.995]
y_seuil_noise = [0.915, 0.92, 0.93, 0.94, 0.945, 0.95, 0.955, 0.96, 0.965, 0.97]

func_coeff_line = np.polyfit(x, y_coeff_line, 4)
func_coeff_noise = np.polyfit(x, y_coeff_noise, 5)
func_seuil_all = np.polyfit(x, y_seuil_all, 4)
func_seuil_noise = np.polyfit(x, y_seuil_noise, 5)


def extract_border_files_in_folder(path_in, path_out, resize_ratio, KEEP_LINE = True, SHOW_BOTH_IMAGES = False):
    if resize_ratio == 1 :
        USE_PARAM_BIG = True
    else : 
        USE_PARAM_BIG = False
    
    if not os.path.exists(path_out):
        os.makedirs(path_out)
    #filesname = YOLO_list_to_extract(path_in)
    filesname = []
    for root, dirs, files in os.walk(path_in, topdown=False):
        for name in files:
            filesname.append(name)
            
    for name in filesname:
        temp_image = cv.imread(path_in + os.sep + name, 0)
        image = cv.resize(temp_image, (0, 0), fx=resize_ratio, fy=resize_ratio)
        out_ima = border_extract_by_noise_and_lines_addition(image, KEEP_LINE, USE_PARAM_BIG )
        
        if SHOW_BOTH_IMAGES : 
            u,v = image.shape
            both_image = np.zeros((u, 2*v))
            both_image[:,:v] = image
            both_image[:,v:] = out_ima
            cv.imwrite(path_out + os.sep + name, both_image)
        else : 
            cv.imwrite(path_out + os.sep + name, out_ima)
    return 0          

def YOLO_list_to_extract(folder):
    model = torch.hub.load('ultralytics/yolov5',  'custom', path='yolov5_model/extract_border/best.pt')
    n = 640
    out_list = []
    for root, dirs, files in os.walk(folder, topdown=False):
        for name in files:
            path_image = os.path.join(root, name)
            image = cv.imread(path_image)
            u, v = image.shape[:2]
                
            img640  = cv.resize(image, (n,n))
            results = model(img640)
            try : 
                prediction = results.xyxy[0][0].numpy()
                if prediction[-1] == 1:
                    out_list.append(name)
            except IndexError :
                print('no classification found, ignored')
    print('there are ', len(out_list),' images to be treated')
    return out_list




def border_extract_by_noise_and_lines_addition(image, KEEP_LINE, BIG_IMA):
    image = cv.filter2D(image, -1, kernel_sharp)

    u, v = image.shape
    padding = np.zeros((u+v, u+v))
    padding[0:u,0:v] = image

    # FFT change of base
    dft_ima = FFT.DFT(padding)
    ima_ph = np.angle(dft_ima)
    ima_mag = np.abs(dft_ima)
    
    # processing in Fourier
    # selecting the noise
    u_filt, v_filt = ima_mag.shape
    filter_ = np.ones((u_filt, v_filt))
    if BIG_IMA : 
        h=int(u_filt//4)
        w = int(u_filt//86)
    else : 
        h=int(u_filt//4)
        w = int(u_filt//86)
    cv.line(filter_, [u_filt//2 -h,v_filt//2], 
                      [u_filt//2 +h,v_filt//2], zeros, w) 
    cv.line(filter_, [u_filt//2,v_filt//2-h], 
                      [u_filt//2,v_filt//2+h], zeros, w)

    radius = int(u_filt//55)
    cv.circle(filter_, [u_filt//2,v_filt//2], radius, zeros, -1)
    filt_ima = np.multiply(ima_mag, filter_)
    
    if not KEEP_LINE :
    # selecting the lines
        filter_ = np.zeros((u_filt, v_filt))
        w = 25
        h=int(u_filt//2)
        cv.line(filter_, [u_filt//2 -h,v_filt//2], 
                              [u_filt//2 +h,v_filt//2], ones, w) 
        cv.line(filter_, [u_filt//2,v_filt//2-h], 
                              [u_filt//2,v_filt//2+h], ones, w)
        radius = 900
        cv.circle(filter_, [u_filt//2,v_filt//2], radius, zeros, -1)
        filt_ima_lines = np.multiply(ima_mag, filter_)
    #print(np.mean(image))
    
    
    crop_center = image[int(u//13):12*int(u//13), int(u//9):8*int(u//9)]
    if np.mean(crop_center) < np.mean(image):
        x = np.mean(crop_center)
    else : 
        x = np.mean(image)
    seuil_all = apply_function(x, func_seuil_all, 0.99)
    coeff_noise =  apply_function(x, func_coeff_noise, 1.5)
    seuil_noise =  apply_function(x, func_seuil_noise, 0.98)
    if not KEEP_LINE : 
        coeff_lines =  apply_function(x, func_coeff_line,1.45)
    
    
    # Reconstruction filtered OG
    reconstr_all = FFT.reconstruct(filt_ima, ima_ph)
    small_reconstr_all  = reconstr_all[0:u,0:v]
    small_reconstr_all = redo_bornes(small_reconstr_all)
    seuil_blanc = np.quantile(small_reconstr_all, seuil_all)
    small_reconstr_all[small_reconstr_all > seuil_blanc] = 255
    # Reconstruction filtered modify (shift)
    reconstr_noise = FFT.reconstruct(np.fft.fftshift(filt_ima), ima_ph)
    small_reconstr_noise  = reconstr_noise[0:u,0:v]
    small_reconstr_noise = redo_bornes(small_reconstr_noise)
    seuil_blanc = np.quantile(small_reconstr_noise, seuil_noise)
    small_reconstr_noise[small_reconstr_noise > seuil_blanc] = 255
    if not KEEP_LINE : 
        #reconstruct lines
        reconstr = FFT.reconstruct(filt_ima_lines, ima_ph)
        small_reconstr_line  = reconstr[0:u,0:v]
        small_reconstr_line = redo_bornes(small_reconstr_line)
    
    summ = image + coeff_noise * small_reconstr_all 
    summ = summ + coeff_noise * small_reconstr_noise 
    if not KEEP_LINE : 
        summ = summ +  coeff_lines * small_reconstr_line
    summ[summ > 255] = 255
    summ = redo_bornes(summ)
    
    return summ
    
    
    
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
