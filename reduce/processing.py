import argparse
from ima_mod import from_tiff, resize_folder

TIFF = 'tiff'
JPG = 'jpeg'
PNG = 'png'
SMALL = 'resize'
LIGHT = 'Architrave'



parser = argparse.ArgumentParser(description="Image Processing")
parser.add_argument("--it", "--image_type", type=str, default="jpg", help="jpg, png")
parser.add_argument("--tiff", type=bool, default=True, help="change type from tiff ?")
parser.add_argument("--res", "--resize", type=bool, default=True, help="resize image ?")
parser.add_argument("--red", "--reduce", type=bool, default=False, help="make a reduce quality image ?")
parser.add_argument("--ra","--ratio", type=float, default=0.2, help="reduction ratio used for resize")

opt = parser.parse_args()

if opt.it.lower() == 'png' : 
    NEW_TYPE = PNG
elif opt.it.lower() == 'jpg' or opt.it.lower() == 'jpeg':
    NEW_TYPE = JPG
else : 
    print('unkown type, will be treated as png')
    NEW_TYPE = PNG
        
if opt.tiff : 
    from_tiff(TIFF, NEW_TYPE, opt.it)
if opt.res : 
    resize_folder(NEW_TYPE, SMALL, LIGHT, opt.ra, opt.red)
