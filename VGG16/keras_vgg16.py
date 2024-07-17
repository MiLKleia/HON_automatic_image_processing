import keras.backend as K
import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv
import pandas as pd
import os
import tensorflow as tf

from keras import models
from keras import optimizers
from tensorflow.keras.applications import VGG16
from keras.preprocessing import image
from keras.applications.vgg16 import preprocess_input
from keras.models import Sequential
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dropout

X_path = 'dataset_crop/X'
datafilis_path = 'dataset_crop/datafile.csv'




def iou_coef(y_true, y_pred, smooth=1):
    """
    IoU = (|X &amp; Y|)/ (|X or Y|)
    """
    intersection = K.sum(K.abs(y_true * y_pred), axis=-1)
    union = K.sum((y_true,-1) + K.sum(y_pred,-1) - intersection)
    return ((intersection + smooth) / ( union + smooth))

# Mean Absolute Error, needs to be change to working IoU
def mav(true, pred):
    diff = abs(true-pred)
    return tf.reduce_mean(diff)
    
    
def iou(true, pred):
    intersection = true * pred
    notTrue = 1 - true
    union = true + (notTrue * pred)
    return K.sum(intersection) / K.sum(union)



# Initialisation
Data_Image = pd.read_csv(datafilis_path,sep=";", on_bad_lines='skip') 
np_Data_Image = Data_Image.to_numpy()

labels_list=[] 
sizes_list = []
filename = []
len_data= len(np_Data_Image)
n_train = 825

for row in np_Data_Image :
    name = row[0]
    path = X_path + name
    filename.append(name)
    startX = float(row[3])/row[1]
    startY = float(row[4])/row[2]
    endX = float(row[5])/row[1]
    endY = float(row[6])/row[2]
    labels_list.append((startX,startY,endX,endY))
    sizes_list.append((row[1],row[2]))
        
labels = np.array(labels_list)
sizes = np.array(sizes_list)
print('labels prepared')

load_model = VGG16(weights='imagenet', include_top=False)
model = VGG16(weights='imagenet', include_top=False)
print(labels[1][0]+1)
model.summary()
train_feature=np.zeros(shape=(n_train,7,7,512))


model = Sequential()
model.add(Flatten(input_shape=train_feature.shape[1:]))
model.add(Dense(4096,activation='relu'))
model.add(Dense(1024, activation='relu'))
model.add(Dense(512, activation='relu'))
model.add(Dense(4, activation='linear'))
sgd = optimizers.SGD(learning_rate=0.001, momentum=0.9, nesterov=True)
model.compile(loss=mav ,optimizer=sgd, metrics=[iou])

counter_pack = 1
c=0    

while counter_pack <= (len_data//n_train):
    for i in range(n_train):
        img_path = X_path + '/' + filename[i+ n_train*(counter_pack -1)]
        img = cv.imread(img_path)
        img_data=cv.resize(img,(224,224))
        img_data = np.expand_dims(img_data, axis=0)
        img_data = preprocess_input(img_data)
        
        #generate a random BB that we will try to correct
        vgg16_feature = load_model.predict(img_data)
        train_feature[c]=vgg16_feature
        c = c+1
    labels_550 = labels[n_train*(counter_pack -1): n_train*counter_pack]
    print('extracting features of pack ', counter_pack, ' done')
    history=model.fit(train_feature, labels_550, epochs=35,batch_size=32)
    print( counter_pack, '[st/nd/rd/th] fit done')
    #reset our data loader
    train_feature=np.zeros(shape=(n_train,7,7,512))
    c=0 
    counter_pack += 1
       
model.save_weights('model.h5')
