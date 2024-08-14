import argparse
import gc
import os
import sys
from typing import List, Tuple
from scipy import ndimage
import skimage.segmentation 

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf

from .data import convert_one_hot_to_image, preprocess_deploy
from .net import deepfloorplanModel
from .net_func import deepfloorplanFunc
from .utils.rgb_ind_convertor import (
    floorplan_boundary_map,
    floorplan_fuse_map,
    ind2rgb,
)
from .utils.settings import overwrite_args_with_toml
from .utils.util import fill_break_line, flood_fill, refine_room_region
import cv2 as cv

os.environ["TF_FORCE_GPU_ALLOW_GROWTH"] = "true"
floorplan_boundary_map = {
    0: [0, 0, 0],  # background
    1: [255, 60, 128],  # opening (door&window)
    2: [255, 255, 255],  # wall line
}


def predict(
    model: tf.keras.Model, img: tf.Tensor, shp: np.ndarray
) -> Tuple[tf.Tensor, tf.Tensor]:
    features = []
    feature = img
    for layer in model.vgg16.layers:
        feature = layer(feature)
        if layer.name.find("pool") != -1:
            features.append(feature)
    x = feature
    features = features[::-1]
    del model.vgg16
    gc.collect()

    featuresrbp = []
    for i in range(len(model.rbpups)):
        x = model.rbpups[i](x) + model.rbpcv1[i](features[i + 1])
        x = model.rbpcv2[i](x)
        featuresrbp.append(x)
    logits_cw = tf.keras.backend.resize_images(
        model.rbpfinal(x), 2, 2, "channels_last"
    )

    x = features.pop(0)
    nLays = len(model.rtpups)
    for i in range(nLays):
        rs = model.rtpups.pop(0)
        r1 = model.rtpcv1.pop(0)
        r2 = model.rtpcv2.pop(0)
        f = features.pop(0)
        x = rs(x) + r1(f)
        x = r2(x)
        a = featuresrbp.pop(0)
        x = model.non_local_context(a, x, i)

    del featuresrbp
    logits_r = tf.keras.backend.resize_images(
        model.rtpfinal(x), 2, 2, "channels_last"
    )
    del model.rtpfinal

    return logits_cw, logits_r

def post_process_wall( bd_ind: np.ndarray, shp: np.ndarray):

    new_bd_ind = fill_break_line(bd_ind).squeeze()
    new_bd_ind = ind2rgb(new_bd_ind.reshape(*shp[:2]), floorplan_boundary_map)
    return new_bd_ind
    
    
def post_process_room(rm_ind, bd_ind, shp, CLEAN = False, MULTI = False):
    if CLEAN : ## SLOW
        fuse_mask = np.zeros(rm_ind.shape)
        fuse_mask[rm_ind > 0] = 255
        fuse_mask = flood_fill(fuse_mask)

        new_rm_ind = fill_fuse_mask(fuse_mask.reshape(*shp[:2]), rm_ind.reshape(*shp[:2]))
        
        bd_ind.reshape(*shp[:2], -1)
        bd_ind = bd_ind[:,:,0]
    else : 
        new_rm_ind = rm_ind
        
    if MULTI : 
        new_rm_ind[bd_ind == 2.] = 10.
        new_rm_ind[bd_ind == 1.] = 9.
    room_final = ind2rgb(new_rm_ind.reshape(*shp[:2]))
    return room_final

def fill_fuse_mask(fuse, rm_ind):
    fuse = fuse.astype('uint8')
    out = fuse
    u, v = rm_ind.shape[:2]
    while len(np.unique(fuse))>1:
        coordinate = np.argwhere(fuse == 255)
        i, j = coordinate[0]
        temp = rm_ind.copy()
        fuse = skimage.segmentation.flood_fill(fuse, (i, j), 127)
        temp[fuse != 127] = 0   
        uni, counts = np.unique(temp, return_counts=True)
        room = uni[np.argwhere(counts == np.max(counts[1:]))]
        out[fuse == 127] = int(room)
        fuse[fuse < 128] = 0 
    return out.astype('float32')
                
    
    



def colorize(r: np.ndarray, cw: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    cr = ind2rgb(r, color_map=floorplan_fuse_map)
    ccw = ind2rgb(cw, color_map=floorplan_boundary_map)
    return cr, ccw


def main(config: argparse.Namespace) -> np.ndarray:
    

    if config.wall : 
        path = "log_wall" + os.sep + "store" + os.sep + "model.tflite"
        model_wall = tf.lite.Interpreter(model_path=path)
        model_wall.allocate_tensors()
    else : 
        path = "log_room" + os.sep + "store" + os.sep + "model.tflite"
        model_room = tf.lite.Interpreter(model_path=path)
        model_room.allocate_tensors()
        path_wall = "log_wall" + os.sep + "store" + os.sep + "model.tflite"
        model_wall = tf.lite.Interpreter(model_path=path_wall)
        model_wall.allocate_tensors()

    
    if not os.path.exists(config.save_folder):
        os.makedirs(config.save_folder)   
        
    for root, dirs, files in os.walk(config.images, topdown=False):
        for name in files:  
            image = os.path.join(root, name)
 
            img = cv.imread(image)
            img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
            shp = img.shape
            img = cv.resize(img, (512,512))
            
            img = tf.convert_to_tensor(img, dtype=tf.uint8)
            img = preprocess_deploy(img)
             
            if config.wall :
                input_details_wall = model_wall.get_input_details()
                output_details_wall = model_wall.get_output_details()
                model_wall.set_tensor(input_details_wall[0]["index"], img)
                model_wall.invoke()
                _, cwi = 0, 1
                if config.tfmodel == "func":
                    ri, cwi = 1, 0
                logits_cw = model_wall.get_tensor(output_details_wall[cwi]["index"])
                logits_cw = tf.convert_to_tensor(logits_cw)
                logits_cw = tf.image.resize(logits_cw, shp[:2])
                cw = convert_one_hot_to_image(logits_cw)[0].numpy()
                

                out = post_process_wall(cw, shp)

            else :
                input_details_wall = model_wall.get_input_details()
                output_details_wall = model_wall.get_output_details()
                model_wall.set_tensor(input_details_wall[0]["index"], img)
                model_wall.invoke()
                _, cwi = 0, 1
                if config.tfmodel == "func":
                    ri, cwi = 1, 0
                logits_cw = model_wall.get_tensor(output_details_wall[cwi]["index"])
                logits_cw = tf.convert_to_tensor(logits_cw)
                logits_cw = tf.image.resize(logits_cw, shp[:2])
                cw = convert_one_hot_to_image(logits_cw)[0].numpy()

                input_details = model_room.get_input_details()
                output_details = model_room.get_output_details()
                model_room.set_tensor(input_details[0]["index"], img)
                model_room.invoke()
                ri, _ = 0, 1
                if config.tfmodel == "func":
                    ri, _ = 1, 0
                logits_r = model_room.get_tensor(output_details[ri]["index"])
                logits_r = tf.convert_to_tensor(logits_r)
    
                logits_r = tf.image.resize(logits_r, shp[:2])
                r = convert_one_hot_to_image(logits_r)[0].numpy()
                


                out = post_process_room(r, cw, shp, config.clean, config.multi)

            mpimg.imsave(os.path.join(config.save_folder, name), out.astype(np.uint8))




def parse_args(args: List[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--tfmodel", type=str, default="subclass", choices=["subclass", "func"]
    )
    p.add_argument("--images", type=str, default="images")
    p.add_argument("--wall", action="store_true")
    p.add_argument("--clean",action="store_true")
    p.add_argument("--multi",action="store_true")
    p.add_argument("--save_folder", type=str, default="outputs")
    p.add_argument(
        "--feature-channels",
        type=int,
        action="store",
        default=[256, 128, 64, 32],
        nargs=4,
    )
    p.add_argument(
        "--backbone",
        type=str,
        default="vgg16",
        choices=["vgg16", "resnet50", "mobilenetv1", "mobilenetv2"],
    )
    p.add_argument(
        "--feature-names",
        type=str,
        action="store",
        nargs=5,
        default=[
            "block1_pool",
            "block2_pool",
            "block3_pool",
            "block4_pool",
            "block5_pool",
        ],
    )
    p.add_argument("--tomlfile", type=str, default=None)
    return p.parse_args(args)


def deploy_plot_res(result: np.ndarray):
    print(result.shape)
    plt.imshow(result)
    plt.xticks([])
    plt.yticks([])
    plt.grid(False)


if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    args = overwrite_args_with_toml(args)
    main(args)
