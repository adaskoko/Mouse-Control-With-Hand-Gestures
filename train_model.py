import cv2
import numpy as np
from keras_squeezenet import SqueezeNet
from keras.optimizers import Adam
from keras.utils import np_utils
from keras.layers import Activation, Dropout, Convolution2D, GlobalAveragePooling2D
from keras.models import Sequential
import tensorflow as tf
import os
import settings


'''Model training based on article:
https://towardsdatascience.com/artificial-neural-networks-for-gesture-recognition-for-beginners-7066b7d771b5'''


IMG_SIZE = settings.Gesture.IMG_SIZE


def def_model_param():
    GESTURE_CATEGORIES = len(CATEGORY_MAP)
    base_model = Sequential()
    base_model.add(SqueezeNet(input_shape=(IMG_SIZE[0], IMG_SIZE[1], 3), include_top=False))
    base_model.add(Dropout(0.5))
    base_model.add(Convolution2D(GESTURE_CATEGORIES, (1, 1), padding='valid'))
    base_model.add(Activation('relu'))
    base_model.add(GlobalAveragePooling2D())
    base_model.add(Activation('softmax'))

    return base_model


def label_mapper(val):
    return CATEGORY_MAP[val]


training_img_folder = 'training_images_3'

CATEGORY_MAP = {
    "move": 0,
    "left_click": 1,
    "right_click": 2,
    "double_left_click": 3,
    "scroll": 4
}

input_data = []
for sub_folder_name in os.listdir(training_img_folder):
    path = os.path.join(training_img_folder, sub_folder_name)
    for fileName in os.listdir(path):
        if fileName.endswith(".jpg"):
            img = cv2.imread(os.path.join(path, fileName))
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = cv2.resize(img, IMG_SIZE)
            input_data.append([img, sub_folder_name])

img_data, labels = zip(*input_data)

labels = list(map(label_mapper, labels))

labels = np_utils.to_categorical(labels)

model = def_model_param()
model.compile(
    optimizer=Adam(lr=0.0001),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

model.fit(np.array(img_data), np.array(labels), epochs=15)

print("Training Completed")

model.save("model_white_bgr_1.h5")
