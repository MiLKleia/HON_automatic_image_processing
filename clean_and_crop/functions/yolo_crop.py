import numpy as np
import cv2 as cv
import os
import pandas as pd
import torch

if not os.sep =='/':
    import pathlib
    temp = pathlib.PosixPath
    pathlib.PosixPath = pathlib.WindowsPath


def YOLO_crop_folder(in_path, out_path, error_path, check_path, model_path, border_bottom):
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    if not os.path.exists(error_path):
        os.makedirs(error_path)
    if not os.path.exists(check_path):
        os.makedirs(check_path)

    model = torch.hub.load('ultralytics/yolov5',  'custom', path=model_path)
    

    n = 640
    for root, dirs, files in os.walk(in_path, topdown=False):
        for name in files:
            string_name = out_path
            path_image = os.path.join(root, name)
            temp_image = cv.imread(path_image)
            u, v = temp_image.shape[:2]
                
            img640  = cv.resize(temp_image, (n,n))
            results = model(img640)
            try : 
                pred = results.xyxy[0][0].numpy()
                x1 = max(0, int(round(pred[0] * v/n - border_bottom//2)))
                y1 = max(0, int(round(pred[1] * u/n - border_bottom//2)))
                x2 = min(v, int(round(pred[2] * v/n + border_bottom//2)))
                y2 = min(u, int(round(pred[3] * u/n)+ border_bottom))
                if x2 <= x1 or y2 <= y1 or x2-x1 < 100 or y2-y1 < 100 :
                    print('invalid BB')
                    string_name = error_path
                    string_name +=  os.sep + name
                    cv.imwrite(string_name, temp_image)
                else : 
                    ima_crop = temp_image[y1:y2,x1:x2,:].copy()
                    string_name +=  os.sep + name
                    
                    check_string_name = check_path +  os.sep + name
                    w=10
                    red = (0,0,252)
                    cv.line(temp_image, [x1+w//2, y1+w//2], [x1+w//2, y2-w//2], red, w)
                    cv.line(temp_image, [x1+w//2, y2-w//2], [x2-w//2, y2-w//2], red, w)
                    cv.line(temp_image, [x2-w//2, y1+w//2], [x2-w//2, y2-w//2], red, w)
                    cv.line(temp_image, [x1+w//2, y1-w//2], [x2-w//2, y1-w//2], red, w)
                    try :
                        cv.imwrite(string_name, ima_crop)
                        cv.imwrite(check_string_name, temp_image)
                    except cv.error :
                        print('error when writting file')
                        print(x1, x2, y1, y2)
                        string_name = error_path
                        string_name +=  os.sep + name
                        cv.imwrite(string_name, temp_image)
            except IndexError :
                print('no BB found')
                string_name = error_path
                string_name +=  os.sep + name
                cv.imwrite(string_name, temp_image)
    return 0
