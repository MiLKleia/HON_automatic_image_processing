import numpy as np
import os
import cv2 as cv
import functions.FFT_functions as FFT



#####  Use set_set_function.py to adapt function
seuil_dark = 190

Data_Image = pd.read_csv('function.csv',sep=";", on_bad_lines='skip') 
func_std = Data_Image.to_numpy()
coeff_std_noisy = np.polyfit(func_std[0], func_std[1], 3)

Data_Image = pd.read_csv('function_dark.csv',sep=";", on_bad_lines='skip') 
func_dark = Data_Image.to_numpy()
coeff_dark_noisy = np.polyfit(func_dark[0], func_dark[1], 3)

"""
func_noisy_x=  np.array([0, 0.05, 0.4, 0.5, 0.62, 0.75, 1])
func_noisy_y = np.array([0, 0.03, 0.25, 0.5, 0.75, 0.9, 1])
coeff_std_noisy = np.polyfit(func_noisy_x, func_noisy_y, 3)

func_dark_noisy_x= np.array([0, 0.05, 0.2, 0.5 , 1])
func_dark_noisy_y = np.array([0, 0.25, 0.5, 0.9, 5])
coeff_dark_noisy = np.polyfit(func_dark_noisy_x, func_dark_noisy_y, 3)
"""

###### DON'T TOUCH

func_dark_x= np.array([0, 0.076389, 0.247685, 0.414452, 0.738426, 1])
func_dark_y = np.array([0, 0.255991, 0.631373, 0.840741, 0.996078, 1])
coeff_dark = np.polyfit(func_dark_x, func_dark_y, 3)

func_std_x= np.array([0, 0.243055, 0.384259, 0.502315, 0.622685, 0.759259, 1])
func_std_y = np.array([0, 0.0394336, 0.212637, 0.490196, 0.765795, 0.937255, 1])
coeff_std_funct = np.polyfit(func_std_x, func_std_y, 3)





def folder_of_ima_to_reduce_greyscale(in_path, out_path, coeff_reduce):
    if not os.path.exists(out_path):
        os.makedirs(out_path)

    for root, dirs, files in os.walk(in_path, topdown=False):
        for name in files:
            string_name = out_path
            path_image = os.path.join(root, name)
            temp_image = cv.imread(path_image, 0)
            temp_image = cv.resize(temp_image, (0, 0), fx=coeff_reduce, fy=coeff_reduce)
            string_name += os.sep + name
            cv.imwrite(string_name, temp_image)

def folder_krita_clean_line_keep(in_path, out_path, noisy = False):
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    counter = 0
    if noisy :
        seuil = seuil_dark
    else : 
        seuil = 190
    
    for root, dirs, files in os.walk(in_path, topdown=False):
        for name in files:
            string_name = out_path
            path_image = os.path.join(root, name)
            
            counter += 1
            if counter%50 == 0:
                print(counter, ' images treated')
            temp_image = cv.imread(path_image, 0)
            if np.quantile(temp_image, 0.7) > seuil and not noisy :
                #Standard function
                temp_image = krita_etalonnage_line_keep(temp_image)
            elif np.quantile(temp_image, 0.7) > seuil and noisy :
                #noisy function
                temp_image = apply_polynomial_function(temp_image, 0, coeff_std_noisy[0] , coeff_std_noisy[1] , coeff_std_noisy[2], 0)
            elif np.quantile(temp_image, 0.3) > 130 and not noisy:
                # mixed function
                temp_image = apply_polynomial_function(temp_image, 0, -3.67725,  3.52125, 1.15599, 0)
            elif noisy:
                #dark function
                temp_image = apply_polynomial_function(temp_image, 0, coeff_dark_noisy[0] , coeff_dark_noisy[1] , coeff_dark_noisy[2], 0)
            else : temp_image = apply_polynomial_function(temp_image, 0, coeff_dark[0] , coeff_dark[1] , coeff_dark[2], 0)
            string_name += os.sep + name
            cv.imwrite(string_name, temp_image)
    print('folder cleaned')           

            
def folder_check_clean(in_path, og_path,  error_path):
    if not os.path.exists(error_path):
        os.makedirs(error_path)
    
    for root, dirs, files in os.walk(in_path, topdown=False):
        for name in files:
            path_image = os.path.join(root, name)
            print(name)
            temp_image = cv.imread(path_image)
            is_okay_image = test_accept_clean(temp_image)
            if not is_okay_image : 
                og_image = cv.imread(og_path + os.sep + name)
                out_path = error_path + os.sep + name
                cv.imwrite(out_path, og_image)
                os.remove(path_image)
    return 0


len_crop = 8 
def test_accept_clean(image):
    mean = np.mean(image)
    median =  np.quantile(image, 0.5)
    if abs(mean-median) < 4.5 :
        return False
    else : 
        u, v = image.shape[:2]
        half_left = image[:,:v//len_crop]
        half_right = image[:,(len_crop-1)*v//len_crop+1:]
        mean_left = np.mean(half_left)
        mean_right = np.mean(half_right)
        if abs(mean_left - mean_right) > 170 : 
            return False
    return True

# make all pixel within 0:255 without calibration
def make_values_okay(post_function_array):
    post_function_array[post_function_array > 1] = 1
    post_function_array[post_function_array < 0] = 0
    post_function_array = post_function_array*255
    post_function_array = post_function_array.astype('uint8')
    return post_function_array
 
# Similar to mean/max/min pooling, you give the quantile you want to be selected.     
def decile_pool(image, kernel_size, decile):
    if len(image.shape) == 3 :
        image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    u,v = image.shape
    
    new_u = int(u/kernel_size) + (u % kernel_size > 0)
    new_v = int(v/kernel_size) + (v % kernel_size > 0)
    
    out = np.zeros((new_u,new_v))
    
    for i in range(new_u):
        for j in range(new_v):
            cropp = image[i*kernel_size:(i+1)*kernel_size-1,
                                    j*kernel_size:(j+1)*kernel_size-1]
            if cropp.shape[0] == 0 :
                out[i,j] = out[i-1,j]
            elif cropp.shape[1] == 0 :
                out[i,j] = out[i,j-1]
            else :
                out[i,j] = np.quantile(cropp, decile)
    return out.astype('uint8')

    
def apply_polynomial_function(image, p4, p3, p2, p1, c):
    norm_arr = 1/255 * image
    x_1 = norm_arr 
    x_2 = np.multiply(norm_arr, norm_arr)
    x_3 = np.multiply(x_2, norm_arr)
    x_4 = np.multiply(x_2, x_2) 
    norm_arr = p1*x_1 + p2*x_2 + p3*x_3 + p4*x_4 + c
    norm_arr = make_values_okay(norm_arr)
    return norm_arr

# Most used polynomial function
def krita_etalonnage_line_keep(image):
    norm_arr = 1/255 *image
    x_1 = norm_arr
    x_2 = np.multiply(x_1, x_1)
    x_3 = np.multiply(x_2, x_1)
    norm_arr = coeff_std_funct[2]*x_1 +coeff_std_funct[1]*x_2 + coeff_std_funct[0]*x_3 + coeff_std_funct[3]
    norm_arr = make_values_okay(norm_arr)
    return norm_arr   
 
