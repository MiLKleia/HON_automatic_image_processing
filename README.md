<h1>Table of Contents<span class="tocSkip"></span></h1>
<div class="toc"><ul class="toc-item"><li><span><a href="#Presentation" data-toc-modified-id="Presentation-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Presentation</a></span></li><li><span><a href="#Clean-and-Crop" data-toc-modified-id="Clean-and-Crop-2"><span class="toc-item-num">2&nbsp;&nbsp;</span>Clean and Crop</a></span><ul class="toc-item"><li><span><a href="#Folders-For-Clean-and-Crop" data-toc-modified-id="Folders-For-Clean-and-Crop-2.1"><span class="toc-item-num">2.1&nbsp;&nbsp;</span>Folders For Clean and Crop</a></span></li><li><span><a href="#Preparation" data-toc-modified-id="Preparation-2.2"><span class="toc-item-num">2.2&nbsp;&nbsp;</span>Preparation</a></span></li><li><span><a href="#Supress-and-extract-info-using-FFT" data-toc-modified-id="Supress-and-extract-info-using-FFT-2.3"><span class="toc-item-num">2.3&nbsp;&nbsp;</span>Supress and extract info using FFT</a></span><ul class="toc-item"><li><span><a href="#Supress-grid" data-toc-modified-id="Supress-grid-2.3.1"><span class="toc-item-num">2.3.1&nbsp;&nbsp;</span>Supress grid</a></span></li><li><span><a href="#Keep-only-wall" data-toc-modified-id="Keep-only-wall-2.3.2"><span class="toc-item-num">2.3.2&nbsp;&nbsp;</span>Keep only wall</a></span></li></ul></li><li><span><a href="#Set-Function" data-toc-modified-id="Set-Function-2.4"><span class="toc-item-num">2.4&nbsp;&nbsp;</span>Set Function</a></span></li></ul></li><li><span><a href="#Reduce" data-toc-modified-id="Reduce-3"><span class="toc-item-num">3&nbsp;&nbsp;</span>Reduce</a></span></li><li><span><a href="#BBR---VGG16" data-toc-modified-id="BBR---VGG16-4"><span class="toc-item-num">4&nbsp;&nbsp;</span>BBR - VGG16</a></span></li><li><span><a href="#Floor-plan-detection" data-toc-modified-id="Floor-plan-detection-5"><span class="toc-item-num">5&nbsp;&nbsp;</span>Floor plan detection</a></span></li><li><span><a href="#YOLO-data-create" data-toc-modified-id="YOLO-data-create-6"><span class="toc-item-num">6&nbsp;&nbsp;</span>YOLO data create</a></span></li></ul></div>

# Presentation

Project realised for Archives Architectures HEPIA.
Aim was to automate the cleaning and cropping of numerisations of plans.

Second aim was to find a way to detect the room of a floor plan [unfinished].

# Clean and Crop
## Folders For Clean and Crop
     
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
        |   +-- Krita_no_line
        |   |   |
        |   |   +-- Roll_NUM
        |   |
        |   +-- extract_contours
        |       |
        |       +-- Roll_NUM
        |
        +-- functions
            |
            +-- clean.py
            +-- [...].py
            +-- models

## Preparation
--tested on Ubuntu 20.10 and Windows 10-- $$\newline$$

Needed for start :  functions and images/OG/reduce_NUM where NUM is a choosen string (int or char). Other folders will be created.
In functions, need YOLO5v trained .pt weights for 640x640 images (we tested using a nano net).
Path to be filled in processing.py line 39 as MODEL_CNN_CROP.

Install needed libraries using : 

        pip install -r requirements.txt 

fill a reduce_NUM folder and launch using :

        python3 processing.py --num_folder "NUM" --treatment "clean_and_crop"

Check crop and clean in images/ML_cropped/check. Delete unsatysfactory from check and run : 

        python3 processing.py --num_folder "NUM" --treatment "redo_fill_folder"
In order to use other cleaning function, follow see Set Function to initialize the function and run :


        python3 processing.py --num_folder "NUM" --treatment "redo_fill_folder" --spe True
Treat images in images/ML_cropped/not_cropped as wanted. Copy to images/ML_cropped/Roll_NUM and run : 

        python3 processing.py --num_folder "NUM" --treatment "compress"
   
Images treated and compressed are in images/compress/Roll_NUM

## Supress and extract info using FFT
DO NOT MODIFY THE IMAGE SIZE, THE FILTERING MAY NOT WORK ANYMORE.
Made to work with images cropped from 2000x24000 images, where wall thickness range from 3 to 10 pixels (can be thicker). Unwanted grid is made of lines with thickness ranging from 1 to 3 pixels.

If no size reduction, RAM of >=16 Go is needed.

### Supress grid
This function uses cleaned images from  images/ML_cropped/Roll_NUM. Run :
    
        python3 processing.py --num_folder "NUM" --treatment "extract_line"
Images are saved in images/Krita_no_line/Roll_NUM

### Keep only wall
This function uses cleaned images from  images/ML_cropped/Roll_NUM. Run :
    
        python3 processing.py --num_folder "NUM" --treatment "extract_all"
Images are saved in images/extract_contours/Roll_NUM



## Set Function

install tkinter and run :

        python3 set_functions.py
A window will open. Top left, select 'outils/trouver approximation'.
On the grid, you can now draw points and an approximation function will be displayed. By default, 4 points are needed to get an approximation. Points can be drawn outside the grid. You can change that number at the the bottom of the window by selecting a value between 2 and 9. When the display function is acceptable, select 'outils/sauvegarder dernier approximation'. A csv file will be save in the functions folder. You can select if the function should be use on dark images or standard images by selecting the 'Fonction pour les images sombres' toggle and repeating thje same steps.

Before runnig processing.py, csv files for both function need to exist in the functions folder. Do not delete default files or older files before running, even if not needed. If missing, set_function.py will recreate those files.

Select an image using "Images/Choisir image de test" and either click on "afficher image" or "Images/prévisualiser la dernière fonction" to observe results you can except using the last plot function.

# Reduce

        |
        +-- tiff
        +-- jpeg
        +-- reduce

Takes all images in TIFF, convert to .jpeg of same size and save in JPEG.
Then, takes all images in JPEG and resize them to 20 percent of OG size in REDUCE.

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

# Floor plan detection

Based on https://github.com/zlzeng/DeepFloorplan/tree/master by Zhiliang ZENG, Xianzhi LI, Ying Kin Yu, and Chi-Wing Fu, Deep Floor Plan Recognition using a Multi-task Network with Room-boundary-Guided Attention, IEEE International Conference on Computer Vision (ICCV), 2019.


(For pepople working on the HON project, See the report for link to the HON dataset and more infos)

The folder given here is an adaptation of the original one so that it is compatible with tensorflow>=2 and other up to date libraries.

Before running to train, create the tfrecord by running

        python3 create_tfrecord.py      
For training, run 

        python3 main.py --epochs "NUM"
Default NUM is 10, recommended is ~200. Avoid running on CPU-only.

Checking the results with the last trained model (stored in pretrained)

        python3 main.py --phase "Test"
Will fill out with the results using images from the train folder.

# YOLO data create

Start

        |
        +-- IMA_OG
            |
            +-- IMA
            +-- MASK
End :        
        
        |
        +-- IMA_OG
        |   |
        |   +-- IMA
        |   +-- MASK
        |   
        +-- NAME.yaml
        |  
        +-- coco128
            |   
            +-- images
            |   |
            |   +-- NAME
            |
            +-- labels
                |
                +-- NAME
                
                
Fill IMA_OG as in exemple then run :

        python3 data_create.py --da ARG --n NAME
Where ARG is "none" by default but can be "mirror" for data augmentation purpose. NAME, the name of the dataset.
