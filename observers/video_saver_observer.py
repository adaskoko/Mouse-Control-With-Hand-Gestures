import os

from observers.observer_dp import Observer
from detection import action_detection as ad
import cv2
import settings

ACTIONS = settings.Gesture.ACTIONS


class VideoSaverObserver(Observer):
    def __init__(self, width, height):
        name = len(os.listdir('videos'))
        self.recording = False
        self.out = cv2.VideoWriter(f'videos/{name}.avi',
                                   cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10, (width, height))

    def update(self, subject: ad.ActionDetector) -> None:
        frame = subject.frame.copy()

        if self.recording:
            self.out.write(frame)

            cv2.putText(frame, 'Recording...', (100, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0))
        else:
            cv2.putText(frame, 'Not recording', (100, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0))

        k = cv2.waitKey(1)
        if k == ord('s'):
            self.recording = not self.recording
            if not self.recording:
                self.out.release()

        cv2.imshow('Video saver', cv2.flip(frame, 1))
