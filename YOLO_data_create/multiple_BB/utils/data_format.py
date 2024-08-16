import cv2 as cv
import os
import numpy as np

import utils.data_labels as labels



def find_points(image):
    u, v = image.shape[0:2]
    image = cv.GaussianBlur(image,(5,5),cv.BORDER_DEFAULT)
    edges = cv.Canny(image, 50, 150, apertureSize=3)
    lines = cv.HoughLinesP(edges, 1,np.pi/180, # Angle resolution in radians
                threshold=10, minLineLength=10, maxLineGap=10)
    values = [u, v, 0, 0]
    
    for points in lines:
        x1,y1,x2,y2=points[0]
        x_min = min(x1, x2)
        x_max = max(x1, x2)
        y_min = min(y1, y2)
        y_max = max(y1, y2)
        if values[0]> x_min :
            values[0] = x_min
        if values[1]> y_min:
            values[1]= y_min
        if values[2]< x_max :
            values[2] = x_max
        if values[3]< y_max:
            values[3]= y_max
    return values


def format_values(values, u, v, string = 'YOLO'):
    if string == 'YOLO' :
        x_center = ((values[0] + values[2]) / 2)/v
        y_center = ((values[1] + values[3]) / 2)/u
        x_len = (values[2] - values[0])/v
        y_len = (values[3] - values[1])/u
        out = [x_center, y_center, x_len, y_len]
    else : 
        out = [values[0], values[2], values[1], values[3]]
    return out



def run_throught_masks(name_OG, path, labels_dict):
    path_masks = path +os.sep+ name_OG
    str_out = ""
    for root, dirs, files in os.walk(path_masks, topdown=False):
        for name in files:
            mask = cv.imread(path_masks + os.sep + name)
            u, v = mask.shape[:2]
            values = find_points(mask)
            YOLO_val = format_values(values, u, v)
            str_out += str(labels.return_label_value(name, labels_dict))
            for val in YOLO_val : 
                str_out +=  " " + str(val) 
            str_out += "\n"
    return str_out
                
def txt_to_txt_mirror(string):
    str_out = ""
    list_str = string.split()
    for step in range(len(list_str)//5) : 
        i = 5*step
        str_out += str(list_str[i])
        str_out += " " + str(1 - float(list_str[i+1]))
        for j in range(3):
            str_out += " " + str(list_str[i + 2 + j])
        str_out += "\n"
    return str_out



def run_throught_images(path_ima, path_mask, path_resize, path_txt, labels_dict, MIRROR = False):
    if not os.path.exists(path_resize):
        os.makedirs(path_resize)
    if not os.path.exists(path_txt):
        os.makedirs(path_txt)

    for root, dirs, files in os.walk(path_ima, topdown=False):
        for name in files:
            # PREPARE IMAGES
            ima = cv.imread(path_ima +os.sep+ name)
            u, v = ima.shape[:2]
            resized = cv.resize(ima, (640, 640), interpolation=cv.INTER_CUBIC)
            cv.imwrite(path_resize +os.sep+ name, resized)
            
            # PREPARE .txt
            folder_name = name[:len(name)-4]
            path_masks = path_mask +os.sep+ folder_name
            txt = run_throught_masks(folder_name, path_mask, labels_dict)
            with open(path_txt + os.sep + folder_name + ".txt", 'w') as f:
                f.write(txt)
                
            if MIRROR :
                mirror = cv.flip(resized, 1)
                path_mirror = path_resize +os.sep+ name.replace(".jpg", "_mirror.jpg")
                cv.imwrite(path_mirror, mirror)
            
            
                txt_mirror = txt_to_txt_mirror(txt)
                with open(path_txt + os.sep + folder_name + "_mirror.txt", 'w') as f:
                    f.write(txt_mirror)
        
        
        
        
 
