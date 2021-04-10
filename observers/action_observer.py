from observers.observer_dp import Observer
from detection import action_detection as ad
from gui import info_window as iw
from collections import deque
import numpy as np
import settings
import pyautogui as mouse

ACTIONS = settings.Gesture.ACTIONS

HAND_QUE_SIZE = settings.Action.HAND_QUE_SIZE
GESTURE_QUE_SIZE = settings.Action.GESTURE_QUE_SIZE
MOUSE_SPEED = settings.Action.MOUSE_SPEED


class ActionObserver(Observer):
    def __init__(self):
        self.info_window = iw.InfoWindow()
        self.hand_pos_que = deque(HAND_QUE_SIZE * [None], HAND_QUE_SIZE)
        self.gesture_que = deque(GESTURE_QUE_SIZE * [0], GESTURE_QUE_SIZE)

        self.action = 0

    def update(self, subject: ad.ActionDetector) -> None:
        self.hand_pos_que.append(subject.hand)
        self.gesture_que.append(subject.gesture)
        self.set_action()
        self.info_window.set_hand_pos(subject.hand)

    def damp_gestures(self):
        gesture = max(set(self.gesture_que), key=self.gesture_que.count)
        gesture_accuracy = self.gesture_que.count(gesture) / len(self.gesture_que)
        if gesture_accuracy >= 0.7:
            return gesture
        return 0

    def set_action(self):
        self.action = self.damp_gestures()

        self.info_window.set_gesture(ACTIONS[self.action])

        if 1 <= self.action <= 3:
            self.gesture_que = deque(GESTURE_QUE_SIZE * [0], GESTURE_QUE_SIZE)

            if self.action == 1:
                self.left_click()
            elif self.action == 2:
                self.right_click()
            else:
                self.double_left_click()
        else:
            if self.action == 0:
                self.move()
            else:
                self.scroll()

    def left_click(self):
        pass
        # mouse.click()

    def right_click(self):
        pass
        # mouse.rightClick()

    def double_left_click(self):
        pass
        # mouse.doubleClick()

    def move(self):
        x_mov, y_mov = self.x_y_movement()

        if x_mov is not None and y_mov is not None:
            x = int((-1) * x_mov[0] * MOUSE_SPEED)
            y = int(y_mov[0] * MOUSE_SPEED)
            mouse.moveRel(x, y)
        pass

    def scroll(self):
        _, y_mov = self.x_y_movement()

        if y_mov is not None:
            y = int(y_mov[0] * MOUSE_SPEED)
            # mouse.hscroll(y)

    def x_y_movement(self):
        xs = []
        ys = []
        labels = []
        index = 0
        for pos in self.hand_pos_que:
            if pos is not None:
                xs.append(pos[0] + int(pos[2] / 2))
                ys.append(pos[1] + int(pos[3] / 2))
                labels.append(index)
                index += 1

        x_movement = None
        y_movement = None
        if len(xs) > HAND_QUE_SIZE / 2:
            x_movement = np.polyfit(labels, xs, deg=1)
            y_movement = np.polyfit(labels, ys, deg=1)

        return x_movement, y_movement
