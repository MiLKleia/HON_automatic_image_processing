import numpy as np
import os
import cv2 as cv

def make_values_okay(post_function_array):
    post_function_array[post_function_array > 1] = 1
    post_function_array[post_function_array < 0] = 0
    post_function_array = post_function_array*255
    post_function_array = post_function_array.astype('uint8')
    return post_function_array
    
    
def apply_polynomial_function_and_save(image, p4, p3, p2, p1, c):
    norm_arr = 1/255 * image
    x_1 = norm_arr 
    x_2 = np.multiply(norm_arr, norm_arr)
    x_3 = np.multiply(x_2, norm_arr)
    x_4 = np.multiply(x_2, x_2) 
    norm_arr = p1*x_1 + p2*x_2 + p3*x_3 + p4*x_4 + c
    norm_arr = make_values_okay(norm_arr)
    return norm_arr
    
    
def prepare_resize(path, size_max):
    try : 
        image = cv.imread(path)
        u, v = image.shape[:2]
        if u > v :
            ratio = (size_max*v)//u
            ima = cv.resize(ima, (ratio, size_max))
        else :
            ratio = (size_max*u)//v 
            image = cv.resize(image, (size_max, ratio))     
    except AttributeError:
        image = 0
    return image
