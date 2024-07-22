import numpy as np
import cv2 as cv
import os

# Compare two folder and fill into redo_ the files from og_ missing in done_
def fill_redo_folder(done_, redo_, og_):
    if not os.path.exists(redo_):
        os.makedirs(redo_)

    name_done = []
    name_redo = []
    name_og = []
    for root, dirs, files in os.walk(done_, topdown=False):
        for name in files:
            name_done.append(name)
    for root, dirs, files in os.walk(redo_, topdown=False):
        for name in files:
            name_redo.append(name)
    for root, dirs, files in os.walk(og_, topdown=False):
        for name in files:
            if name not in name_done :
                if name not in name_redo : 
                    image = cv.imread(og_+os.sep+name)
                    cv.imwrite(redo_+os.sep+name, image)
    return 0

# compress or copy all the files of a folder into another one 
def compress_jpg(in_path, out_path):
    if not os.path.exists(out_path):
        os.makedirs(out_path)

    for root, dirs, files in os.walk(in_path, topdown=False):
        for name in files:
            path_image = os.path.join(root, name)
            file_size = os.stat(path_image)
            
            if file_size.st_size > 1000000 : 
                ima = cv.imread(path_image)
                cv.imwrite(out_path +  os.sep + name, ima, [cv.IMWRITE_JPEG_QUALITY, 75])
            elif file_size.st_size > 650000 : 
                ima = cv.imread(path_image)
                cv.imwrite(out_path +  os.sep + name, ima, [cv.IMWRITE_JPEG_QUALITY, 85])
            else :
                ima = cv.imread(path_image)
                cv.imwrite(out_path +  os.sep + name, ima)
    return 0
        
        
#check mean and differents quantile of sizes of images in folder     
def test_mean(in_path):
    list_size = []
    for root, dirs, files in os.walk(in_path, topdown=False):
        for name in files:
            path_image = os.path.join(root, name)
            file_size = os.stat(path_image)
            list_size.append(file_size.st_size) 
    array_size = np.array(list_size)
    
    return [np.mean(array_size), np.quantile(array_size, 0.5), 
            np.quantile(array_size, 0.1), np.quantile(array_size, 0.9)]
