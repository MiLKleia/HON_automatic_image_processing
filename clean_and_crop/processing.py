import numpy as np
import math
import cv2 as cv
import os
import imutils as imutils
import argparse

import functions.FFT_functions as FFT
import functions.yolo_crop as yolo
import functions.sobel_crop as sobel_crop
import functions.clean as clean
import functions.seperate_and_compress as final_steps
import functions.FFT_extract as extract
import functions.FFT_line_erase as line_erase



parser = argparse.ArgumentParser(description="Image Processing")
parser.add_argument("--num", "--num_folder", type=str, default="001", help="Number of the folder to be treated")
parser.add_argument("--t","--treatment", type=str, default="clean_and_crop", help="[reduce_size, clean_and_crop, redo_fill_folder, compress, extract_line, extract_all]")
parser.add_argument("--r","--ratio", type=float, default=0.4, help="reduction ratio used for reduce and FFT function")
parser.add_argument("--spe", "--special", type=bool, default=False, help="Do the image need to use the adapted cleaning function ? Modify in")
parser.add_argument("--c", "--clean", type=bool, default=False, help="Fill the redo folder with the cleaned images")
opt = parser.parse_args()


num_folder = opt.num
FOLDER_ALL_IMAGES = 'images'
FOLDER_OG_IMG = FOLDER_ALL_IMAGES  + os.sep + 'Roll' + os.sep + 'HON_roll_' + num_folder
FOLDER_OG_IMG_REDUCE_SIZE = FOLDER_ALL_IMAGES  + os.sep + 'OG' + os.sep + 'reduce_' + num_folder
FOLDER_CLEAN_IMG = FOLDER_ALL_IMAGES  + os.sep + 'Krita_clean' + os.sep + 'Roll_' + num_folder
FOLDER_CROPPED_ML_IMG = FOLDER_ALL_IMAGES  + os.sep + 'ML_cropped' + os.sep + 'Roll_' + num_folder
FOLDER_CROP_ERROR_REDO = FOLDER_ALL_IMAGES  + os.sep + 'ML_cropped' + os.sep + 'not_cropped'
FOLDER_CROP_CHECK = FOLDER_ALL_IMAGES  + os.sep + 'ML_cropped' + os.sep + 'check'
FOLDER_COMPRESS = FOLDER_ALL_IMAGES  + os.sep + 'compress' + os.sep + 'Roll_' + num_folder

FOLDER_LINE_EXTRACT = FOLDER_ALL_IMAGES + os.sep + 'Krita_no_line' + os.sep + 'Roll_' + num_folder
FOLDER_BORDER_EXTRACT = FOLDER_ALL_IMAGES + os.sep + 'extract_contours' + os.sep + 'Roll_' + num_folder

MODEL_CNN_CROP ='functions' + os.sep + 'models' + os.sep + '640_s_40' + os.sep + 'best.pt'

################################################################################ REDUCE SIZE

coeff = opt.r  #recommended 0.3

if opt.t ==  'reduce_size':
    clean.folder_of_ima_to_reduce_greyscale(in_path = FOLDER_OG_IMG, 
                               out_path = FOLDER_OG_IMG_REDUCE_SIZE, coeff_reduce = coeff)

################################################################################ CLEANING

if opt.t ==  'clean_and_crop':
    clean.folder_krita_clean_line_keep(in_path = FOLDER_OG_IMG_REDUCE_SIZE, 
                                            out_path = FOLDER_CLEAN_IMG, noisy=opt.spe)


################################################################################ Crop ML

if opt.t ==  'clean_and_crop': 
    yolo.YOLO_crop_folder(FOLDER_CLEAN_IMG, FOLDER_CROPPED_ML_IMG, 
                                FOLDER_CROP_ERROR_REDO, FOLDER_CROP_CHECK, MODEL_CNN_CROP, 15)

################################################################################ Load image to redo 

if opt.t ==  'redo_fill_folder': 
    if not opt.c : 
        final_steps.fill_redo_folder(FOLDER_CROP_CHECK, FOLDER_CROP_ERROR_REDO, FOLDER_OG_IMG_REDUCE_SIZE )
    else : 
        final_steps.fill_redo_folder(FOLDER_CROP_CHECK, FOLDER_CROP_ERROR_REDO, FOLDER_CLEAN_IMG )

################################################################################ compress 

if opt.t ==  'compress':
    final_steps.compress_jpg(FOLDER_CROPPED_ML_IMG, FOLDER_COMPRESS)

################################################################################ CLEANING FFT no line

if opt.t ==  'extract_line':
    line_erase.line_erase_files_in_folder(FOLDER_CROPPED_ML_IMG, FOLDER_LINE_EXTRACT, opt.ratio)

################################################################################ FFT Border Extract

if opt.t ==  'extract_all':
    extract.extract_border_files_in_folder(FOLDER_CROPPED_ML_IMG, FOLDER_BORDER_EXTRACT, opt.ratio,
                    KEEP_LINE = False)


