import numpy as np
import math
import cv2 as cv
import os
import imutils as imutils
import argparse

import utilis.FFT_functions as FFT
import utilis.yolo_crop as yolo
import utilis.sobel_crop as sobel_crop
import utilis.clean as clean
import utilis.seperate_and_compress as final_steps
import utilis.FFT_extract as extract
import utilis.FFT_line_erase as line_erase



parser = argparse.ArgumentParser(description="Image Processing")
parser.add_argument("--num_folder", "--num", type=str, default="001", help="Number of the folder to be treated")
parser.add_argument("--treatment","--t", type=str, default="clean_and_crop", help="[reduce_size, clean_and_crop, redo_fill_folder, compress, extract_line, extract_all]")
parser.add_argument("--ratio","--r", type=float, default=0.4, help="reduction ratio used for reduce and FFT function")
parser.add_argument("--special", "--spe", type=bool, default=False, help="Do the image need to use the adapted cleaning function ? Modify in")
opt = parser.parse_args()


num_folder = opt.num_folder
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

MODEL_CNN_CROP ='utilis' + os.sep + 'models' + os.sep + '640_s_40' + os.sep + 'best.pt'

################################################################################ REDUCE SIZE

coeff = opt.ratio  #recommended 0.3

if opt.treatment ==  'reduce_size':
    clean.folder_of_ima_to_reduce_greyscale(in_path = FOLDER_OG_IMG, 
                               out_path = FOLDER_OG_IMG_REDUCE_SIZE, coeff_reduce = coeff)

################################################################################ CLEANING

if opt.treatment ==  'clean_and_crop':
    clean.folder_krita_clean_line_keep(in_path = FOLDER_OG_IMG_REDUCE_SIZE, 
                                            out_path = FOLDER_CLEAN_IMG, noisy=opt.noisy)


################################################################################ Crop ML

if opt.treatment ==  'clean_and_crop': 
    yolo.YOLO_crop_folder(FOLDER_CLEAN_IMG, FOLDER_CROPPED_ML_IMG, 
                                FOLDER_CROP_ERROR_REDO, FOLDER_CROP_CHECK, MODEL_CNN_CROP, 15)

################################################################################ Load image to redo 

if opt.treatment ==  'redo_fill_folder':
    final_steps.fill_redo_folder(FOLDER_CROP_CHECK, FOLDER_CROP_ERROR_REDO, FOLDER_CLEAN_IMG )
    #final_steps.fill_redo_folder(FOLDER_CROP_CHECK, FOLDER_CROP_ERROR_REDO, FOLDER_OG_IMG_REDUCE_SIZE )

################################################################################ compress 

if opt.treatment ==  'compress':
    final_steps.compress_jpg(FOLDER_CROPPED_ML_IMG, FOLDER_COMPRESS)

################################################################################ CLEANING FFT no line

if opt.treatment ==  'extract_line':
    line_erase.line_erase_files_in_folder(FOLDER_CROPPED_ML_IMG, FOLDER_LINE_EXTRACT, opt.ratio)

################################################################################ FFT Border Extract

if opt.treatment ==  'extract_all':
    extract.extract_border_files_in_folder(FOLDER_CROPPED_ML_IMG, FOLDER_BORDER_EXTRACT, opt.ratio,
                    KEEP_LINE = False)


