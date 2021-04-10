from detection import hand_detection as hd
from detection import gesture_detection as gd
from observers.observer_dp import *


class ActionDetector(Subject):
    def attach(self, observer: Observer) -> None:
        self.observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self.observers.remove(observer)

    def notify(self) -> None:
        for obs in self.observers:
            obs.update(self)

    def __init__(self):
        self.hand_detector = hd.HandDetector()
        self.gesture_detector = gd.GestureDetector()
        self.hand = None
        self.previous_hand = None
        self.gesture = None
        self.gesture_area = None
        self.observers = []
        self.frame = None

    def detect_action(self, frame):
        self.frame = frame
        self.hand_detector.detect_hands(frame)

        self.hand = self.hand_detector.get_hand()
        self.previous_hand = self.hand

        (x, y, w, h) = self.hand
        max_dim = max(w, h)
        x = int(max(0, x - (max_dim * 3 - w) / 2))
        y = int(max(0, y - max_dim * 1.5))
        w = int(min(max_dim*3, frame.shape[1] - x))
        h = int(min(max_dim*3, frame.shape[0] - y))

        self.gesture_area = (x, y, w, h)

        self.gesture_detector.detect_gesture(frame[y: y+max(h, 1), x: x+max(w, 1)])
        self.gesture = self.gesture_detector.get_gesture()

        if not self.hand_detector.hand_detected():
            self.hand = None
