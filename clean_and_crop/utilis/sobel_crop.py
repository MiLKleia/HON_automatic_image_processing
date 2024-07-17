import numpy as np
import math
import cv2 as cv
import os


def folder_of_ima_to_crop_SOBEL(in_path, out_path, error_path,  eps, bord):
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    if not os.path.exists(error_path):
        os.makedirs(error_path)

    for root, dirs, files in os.walk(in_path, topdown=False):
        for name in files:
            print(name)
            path_image = os.path.join(root, name)
            image = cv.imread(path_image)
            u, v = image.shape[:2]
             
            no_error = True
            
            try : 
                a, b = get_2nd_border_coordinate(image, eps)
            except TypeError:
                no_error = False
            try :
                #image_extract_vertical = sobel_extract_line(image, True)
                c, d = get_2nd_border_coordinate(image, eps, horizontal = False)
            except TypeError:
                no_error = False
            if b - a < 50 or d - c < 50 : 
                no_error = False
                
            if no_error : 
                c = max(0, c-bord)
                a = max(0, a-bord)
                b = min(b+bord, v)
                d = min(d+2*bord, u)
                out = image[c:d, a:b]
                name_out = out_path + os.sep + name
                cv.imwrite(name_out, out)
            else : 
                out = image
                name_out = error_path + os.sep + name
                cv.imwrite(name_out, out)
    return 0


def sobel_extract_line(image_in, horizontal = True):
    u, v = image_in.shape[0:2]
    
    if len(image_in.shape)==3:
        image_gray = cv.cvtColor(image_in, cv.COLOR_BGR2GRAY)
    else :
        image_gray = image_in.copy()
    blurred = cv.GaussianBlur(image_gray,(3,3),cv.BORDER_DEFAULT)

    kernel = np.ones((5,5), np.uint8)
    image = cv.erode(blurred, kernel, iterations=4)
    
    kernel = np.ones((3,3), np.uint8)
    image = cv.dilate(image, kernel, iterations=3)
    
    if horizontal : 
        kernel = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
        filtr1 = cv.filter2D(image, -1, kernel)
        kernel = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]])
        filtr2 = cv.filter2D(image, -1, kernel)
    else : 
        kernel = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
        filtr1 = cv.filter2D(image, -1, kernel)
        kernel = np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]])
        filtr2 = cv.filter2D(image, -1, kernel)
    image = filtr1 + filtr2 
    image.astype('uint8')
        
    image_color = cv.cvtColor(image, cv.COLOR_GRAY2BGR)
    return image_color

def get_2nd_border_coordinate(image_og, eps, horizontal = True):
    image = sobel_extract_line(image_og, horizontal)
    h, w = image.shape[:2] 
    
    edges = cv.Canny(image_og, 100, 150, apertureSize=3)
    lines = cv.HoughLinesP(edges, 1,np.pi/180, # Angle resolution in radians
                threshold=200, minLineLength=200, maxLineGap=50)
    
    if horizontal : 
        value_ref = [w, w, 0, 0]
        compared_len = w
    else :
        value_ref = [h, h, 0, 0]
        compared_len = h
    try :
        for points in lines:
            # Extracted points nested in the list
            if horizontal :
                to_test_value1, _, to_test_value2, _ = points[0]
            else : 
                _, to_test_value1, _, to_test_value2 = points[0]
            
            if (abs(to_test_value1 - to_test_value2)) < 30 :
            # we only check horizontal or vertical segment
                for x in [to_test_value1, to_test_value2] : 
                    if x < value_ref[1] : 
                        # x smaller than smallest x recorded and diff over eps
                        if value_ref[0] - x > eps :
                            value_ref[1] = value_ref[0]
                            value_ref[0] = x
                        # x smaller than smallest x recorded but diff less than eps    
                        elif value_ref[0] > x :
                            value_ref[0] = x
                        # x smaller tham 2nd smallest x and bigger than smallest x 
                        # such as diff > eps
                        elif x - value_ref[0] > eps :
                            value_ref[1] = x

                    if x > value_ref[2] : 
                        # x bigger than biggest x recorded and diff over eps
                        if x - value_ref[3] > eps :
                            value_ref[2] = value_ref[3]
                            value_ref[3] = x
                        # x bigger than biggest x recorded but diff less than eps    
                        elif value_ref[3] < x :
                            value_ref[3] = x
                        # x bigger than 2nd biggest x and smaller than biggest x 
                        # such as diff > eps
                        elif value_ref[3] - x > eps :
                            value_ref[2] = x
                        
        min_ = max(0, value_ref[1])
        max_ = min(compared_len, value_ref[2])
                
        out = [min_, max_]
        
        return out
    except TypeError :
        return [0, compared_len]

