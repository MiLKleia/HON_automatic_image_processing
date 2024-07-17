<h1>Table of Contents<span class="tocSkip"></span></h1>
<div class="toc"><ul class="toc-item"><li><span><a href="#Presentation" data-toc-modified-id="Presentation-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Presentation</a></span></li><li><span><a href="#Reduce" data-toc-modified-id="Reduce-2"><span class="toc-item-num">2&nbsp;&nbsp;</span>Reduce</a></span></li><li><span><a href="#Clean-and-Crop" data-toc-modified-id="Clean-and-Crop-3"><span class="toc-item-num">3&nbsp;&nbsp;</span>Clean and Crop</a></span><ul class="toc-item"><li><span><a href="#Folder" data-toc-modified-id="Folder-3.1"><span class="toc-item-num">3.1&nbsp;&nbsp;</span>Folder</a></span></li><li><span><a href="#Preparation" data-toc-modified-id="Preparation-3.2"><span class="toc-item-num">3.2&nbsp;&nbsp;</span>Preparation</a></span></li></ul></li><li><span><a href="#BBR---VGG16" data-toc-modified-id="BBR---VGG16-4"><span class="toc-item-num">4&nbsp;&nbsp;</span>BBR - VGG16</a></span></li><li><span><a href="#TODO-:-Floor-plan-detection" data-toc-modified-id="TODO-:-Floor-plan-detection-5"><span class="toc-item-num">5&nbsp;&nbsp;</span>TODO : Floor plan detection</a></span></li></ul></div>

# Presentation

Project realised for Archives Architectures HEPIA.
Aim was to automate the cleaning and cropping of numerisations of plans.

Second aim was to find a way to detect the room of a floor plan [unfinished].

# Reduce

        |
        +-- tiff
        +-- jpeg
        +-- reduce

Takes all images in TIFF, convert to .jpeg of same size and save in JPEG.
Then, takes all images in JPEG and resize them to 20 percent of OG size in REDUCE.

# Clean and Crop
## Folder
     
        |
        +-- images
        |   |
        |   +-- OG
        |   |   | 
        |   |   +--reduce_NUM
        |   |
        |   +-- Krita_clean
        |   |   |
        |   |   +-- Roll_NUM
        |   |
        |   +-- ML_cropped
        |   |   |
        |   |   +-- check
        |   |   +-- Roll_NUM
        |   |   +-- not_cropped
        |   |
        |   +-- compress
        |       |
        |       +-- Roll_NUM
        |
        +-- utilis
            |
            +-- clean.py
            +-- [...].py
            +-- models

## Preparation
--tested on Ubuntu 20.10 and Windows 10-- $$\newline$$

Needed for start :  utilis and images/OG/reduce_NUM. Other folders will be created.
In utilis, need YOLO5v trained .pt weights for 640$\times$640 images (we tested using a nano net).
Path to be filled in processing.py line 39 as MODEL_CNN_CROP.

$\newline$

fill a reduce_NUM folder and launch using :

        python3 processing.py --num_folder "NUM" --treatment "clean_and_crop"

Check crop and clean in images/ML_cropped/check. Delete unsatysfactory from check and run : 

        python3 processing.py --num_folder "NUM" --treatment "redo_fill_folder"

Treat images in images/ML_cropped/not_cropped as wanted. Copy to images/ML_cropped/Roll_NUM and run : 

        python3 processing.py --num_folder "NUM" --treatment "compress"
   
Images treated and compressed are in images/compress/Roll_NUM

# BBR - VGG16

        |
        +-- dataset_crop
            |
            +-- X
            +-- datafile.csv


(Unused method, we recommend using YOLO)
Based on https://github.com/sabhatina/bounding-box-Regression
  
in datafile.csv, data must be :

        name; width; heigh; width top corne; heigh top corner; width bottom corne; heigh bottom corner
where name is the name of an image in X.

To start training, run : 

        python3 keras_VGG.py
        
Weights are save in 'model.h5'.

# TODO : Floor plan detection

Based on https://github.com/SaoYan/DnCNN-PyTorch/tree/master

