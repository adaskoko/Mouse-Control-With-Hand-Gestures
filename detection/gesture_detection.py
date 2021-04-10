from keras.models import load_model
import cv2
import numpy as np

import settings


IMG_SIZE = settings.Gesture.IMG_SIZE

CATEGORY_MAP = settings.Gesture.ACTIONS


def mapper(val):
    return CATEGORY_MAP[val]


class GestureDetector:
    def __init__(self):
        self.model = load_model("models/model_white_bgr_1.h5")
        self.prediction = 0

    def detect_gesture(self, frame):
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, IMG_SIZE)
        prediction = self.model.predict(np.array([img]))

        self.prediction = np.argmax(prediction[0])

    def get_gesture(self):
        return self.prediction
