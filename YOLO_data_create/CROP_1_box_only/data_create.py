import cv2 as cv
import os
import numpy as np
import argparse


parser = argparse.ArgumentParser(description="YOLO : data prepare")
parser.add_argument("--da", "--datd_augmentation", type=str, default="none", help="type of augmentation, [none, mirror]")
parser.add_argument("--n","--name", type=str, default='exemple', help="name of the folder")
opt = parser.parse_args()



DATASET_NAME = opt.n

IMAGE_RESIZE = "coco128"+ os.sep + "images" + os.sep + DATASET_NAME
LABELS = "coco128"+ os.sep + "labels" + os.sep + DATASET_NAME

if not os.path.exists(IMAGE_RESIZE):
    os.makedirs(IMAGE_RESIZE)
if not os.path.exists(LABELS):
    os.makedirs(LABELS)

OG_IMA = "IMA_OG" + os.sep + "IMA"
MASK = "IMA_OG" + os.sep + "MASK"



def find_points(image):
    u, v = image.shape[0:2]
    image = cv.GaussianBlur(image,(5,5),cv.BORDER_DEFAULT)
    edges = cv.Canny(image, 50, 150, apertureSize=3)
    lines = cv.HoughLinesP(edges, 1,np.pi/180, # Angle resolution in radians
                threshold=150, minLineLength=10, maxLineGap=10)
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


for root, dirs, files in os.walk(OG_IMA, topdown=False):
    for name in files:
        path_mask = MASK +os.sep+name
        path_ima = OG_IMA +os.sep+name
        
        mask = cv.imread(path_mask)
        ima = cv.imread(path_ima)
        
        u, v = ima.shape[:2]
        values = find_points(mask)
        #print(values)
        x_center = ((values[0] + values[2]) / 2)/v
        y_center = ((values[1] + values[3]) / 2)/u
        x_len = (values[2] - values[0])/v
        y_len = (values[3] - values[1])/u
        
        path_resize = IMAGE_RESIZE + os.sep + name
        resized = cv.resize(ima, (640, 640), interpolation=cv.INTER_CUBIC)
        cv.imwrite(path_resize, resized)
        
        path_txt = LABELS + os.sep + name.replace('.jpg', '.txt')
        string = "0 "+ str(x_center) + " " + str(y_center) + " "
        string += str(x_len) + " " + str(y_len)
        with open(path_txt, 'w') as f:
            f.write(string)
        
        if opt.da == "mirror" :
            mirror = cv.flip(resized, 1)
            path_mirror = IMAGE_RESIZE + os.sep + name.replace(".jpg", "_mirror.jpg")
            cv.imwrite(path_mirror, mirror)
            
            path_txt_mirror = LABELS + os.sep + name.replace('.jpg', '_mirror.txt')
            string = "0 "+ str(1-x_center) + " " + str(y_center) + " "
            string += str(x_len) + " " + str(y_len)
            with open(path_txt_mirror, 'w') as f:
                f.write(string)
        
### create the yaml

string_yaml = "# Example usage: python train.py --data own_data.yaml\n# parent\n# ├── yolov5\n# └── datasets"
string_yaml += "\n#     └── mine  \n\npath: .." + os.sep + "datasets" + os.sep + "coco128 # dataset root dir\ntrain: images" + os.sep + ""
string_yaml +=  str(DATASET_NAME) + "\nval: images" + os.sep + "" + str(DATASET_NAME)
string_yaml += "\ntest: # test images (optional) \n\n# Classes\nnames:\n  0: crop"
string_yaml += "\n\n# Download script/URL (optional)\n#download: https://ultralytics.com/assets/"

with open(DATASET_NAME + ".yaml", 'w') as f:
    f.write(string_yaml)

