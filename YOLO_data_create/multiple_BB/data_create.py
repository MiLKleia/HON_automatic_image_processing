import argparse
import os

import utils.data_format as form
import utils.data_labels as labels

# Default values. 
DATASET_NAME = 'exemple'
CSV = 'data.csv'
IMA_OG = 'IMA_OG/IMA'
IMA_MASK = 'IMA_OG/MASK'

# will mimic the architecture of dataset. Copy folders as shown.
IMA_RESIZED = "coco128"+ os.sep + "images" 
TXT = "coco128"+ os.sep + "labels"



parser = argparse.ArgumentParser(description="YOLO : data prepare")
parser.add_argument("--n","--name", type=str, default=DATASET_NAME, help="name to be given to dataset")
parser.add_argument("--og", type=str, default=IMA_OG, help="folder of OG images")
parser.add_argument("--masks", type=str, default=IMA_MASK, help="folder of masks images")
parser.add_argument("--data", type=str, default=CSV, help="path to csv")
parser.add_argument("--mi","--mirror", action="store_true", help="datd augmentation with creation of mirrored images.")
opt = parser.parse_args()

LABELS_DICT = labels.load_dictionnary(opt.data)
form.run_throught_images(opt.og, opt.masks, IMA_RESIZED + os.sep + opt.n, TXT + os.sep + opt.n, LABELS_DICT, opt.mi)
labels.YAML_create(LABELS_DICT, opt.n)
