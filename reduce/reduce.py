import numpy as np
import os
import cv2 as cv


TIFF = 'tiff'
JPG = 'jpeg'
SMALL = 'reduce'


for root, dirs, files in os.walk(TIFF, topdown=False):
    for name in files:
        path_image = os.path.join(root, name)
        temp_image = cv.imread(path_image, 0)
        a = np.min(temp_image)
        b = np.max(temp_image)
        if a < b : 
            temp_image = (temp_image-a)/(b-a) * 255
            temp_image  = temp_image.astype(np.uint8)
        path_out = JPG + os.sep + name.replace('.tif', '.jpg')
        cv.imwrite(path_out, temp_image)
        
        
        
for root, dirs, files in os.walk(JPG, topdown=False):
    for name in files:
        path_image = os.path.join(root, name)
        temp_image = cv.imread(path_image, 0)
        temp_image = cv.resize(temp_image, (0, 0), fx=0.2, fy=0.2)
        path_out = SMALL + os.sep + name.replace('.jpg', '_reduit.jpg')
        cv.imwrite(path_out, temp_image)
