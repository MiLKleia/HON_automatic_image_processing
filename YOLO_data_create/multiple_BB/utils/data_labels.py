import cv2 as cv
import os
import numpy as np
import pandas as pd

def load_dictionnary(path):
    Data_Image = pd.read_csv(path,sep=",", on_bad_lines='skip') 
    np_Data_Image = Data_Image.to_numpy()
    labels_dict = {}
    for name, value in np_Data_Image : 
        labels_dict[str(name)] = str(value)
    return labels_dict
    
    
def YAML_create(labels_dict, DATASET_NAME):
    string_yaml = "# Example usage: python train.py --data own_data.yaml\n# parent\n# ├── yolov5\n# └── datasets"
    string_yaml += "\n#     └── mine  \n\npath: .." + os.sep + "datasets" 
    string_yaml += os.sep + "coco128 # dataset root dir\ntrain: images" + os.sep + ""
    string_yaml +=  str(DATASET_NAME) + "\nval: images" + os.sep + "" + str(DATASET_NAME)
    string_yaml += "\ntest: # test images (optional) \n\n# Classes\nnames:\n"
    for name in labels_dict.keys() : 
        string_yaml += "  " + str(labels_dict[name]) + ": " + str(name) + "\n"
        
    string_yaml += "\n\n# Download script/URL (optional)\n#download: https://ultralytics.com/assets/"

    with open(DATASET_NAME + ".yaml", 'w') as f:
        f.write(string_yaml)
        
        
def return_label_value(string, labels_dict):
    name = ""
    word_found = False
    for letter in string : 
        if not word_found and letter != '_' : 
            name += letter
        else :
            word_found = True
    if name in labels_dict : 
        out = labels_dict[name]
    else :
        out = -1
    return out
        
