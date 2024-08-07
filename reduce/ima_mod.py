import numpy as np
import os
import cv2 as cv




def from_tiff(folder_TIFF, folder_out, type_ima):
    if type_ima == 'png' or type_ima == 'jpg':
        str_type = '.' + type_ima.lower()
    else : 
        str_type = '.png'        
    if not os.path.exists(folder_out):
        os.makedirs(folder_out)
        
    for root, dirs, files in os.walk(folder_TIFF, topdown=False):
        for name in files:
            path_image = os.path.join(root, name)
            temp_image = cv.imread(path_image)
            a = np.min(temp_image)
            b = np.max(temp_image)
            if a < b : 
                temp_image = (temp_image-a)/(b-a) * 255
                temp_image  = temp_image.astype(np.uint8)
            path_out =  os.path.join(folder_out, name.replace('.tiff', str_type))
            cv.imwrite(path_out, temp_image)


def resize_folder(folder_in, folder_out, folder_reduce, ratio, reduce_):
    if not os.path.exists(folder_out) and ratio !=1:
        os.makedirs(folder_out)
        
    for root, dirs, files in os.walk(folder_in, topdown=False):
        for name in files:
            if name[len(name)-3:] =='jpg':
                IS_JPG = True
            else :
                IS_JPG = False
            
            path_image = os.path.join(root, name)
            temp_image = cv.imread(path_image)
            if ratio != 1 : 
                temp_image = cv.resize(temp_image, (0, 0), fx=ratio, fy=ratio)
                path_out = os.path.join(folder_out, name)
                cv.imwrite(path_out, temp_image)
            if reduce_ :
                if not os.path.exists(folder_reduce):
                    os.makedirs(folder_reduce)
                red_path_out = folder_reduce + os.sep + name
                if IS_JPG:
                    cv.imwrite(red_path_out, temp_image, [cv.IMWRITE_JPEG_QUALITY, 86])
                else :
                    cv.imwrite(red_path_out, temp_image, [cv.IMWRITE_PNG_COMPRESSION, 70])











        
        
        

        
