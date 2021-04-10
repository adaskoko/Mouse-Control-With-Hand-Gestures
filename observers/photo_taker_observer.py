import os

from observers.observer_dp import Observer
from detection import action_detection as ad
import cv2
import settings

ACTIONS = settings.Gesture.ACTIONS


class PhotoTakerObserver(Observer):
    def __init__(self):
        image_label = 'scroll'
        self.num_of_images = 20

        self.click = False

        training_img_folder = 'training_images_3'

        self.label_name = os.path.join(training_img_folder, image_label)

        # count of images to be captured
        self.count = self.image_name = 0

        try:
            os.mkdir(training_img_folder)
        except FileExistsError:
            pass
        try:
            os.mkdir(self.label_name)
        except FileExistsError:
            # If any images are already present, updating the image name starting number
            self.image_name = len(os.listdir(self.label_name))

    def update(self, subject: ad.ActionDetector) -> None:
        frame = subject.frame.copy()
        if subject.gesture_area is not None:
            (x, y, w, h) = subject.gesture_area
            if self.count == self.num_of_images:
                self.click = False
                self.count = 0
                print('zapisano')
            if self.click:
                region_of_interest = frame[y: y+h, x:x+w]
                save_path = os.path.join(self.label_name, '{}.jpg'.format(self.image_name + 1))
                cv2.imwrite(save_path, region_of_interest)
                self.image_name += 1
                self.count += 1

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)

        k = cv2.waitKey(100)
        if k == ord('s'):
            self.click = not self.click

        cv2.imshow('Photo taker', cv2.flip(frame, 1))
