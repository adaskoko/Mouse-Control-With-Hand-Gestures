import cv2


def get_biggest_hand(hands):
    return max(hands, key=lambda hand: hand[3])


class HandDetector:
    def __init__(self):
        self.hand_cascade = cv2.CascadeClassifier('cascades/hand.xml')
        self.previous_hand_pos = (0, 0, 0, 0)
        self.hand = (0, 0, 0, 0)
        self.hands = ()

    def detect_hands(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        self.hands = self.hand_cascade.detectMultiScale(gray, 1.5, 2)

        if self.hand_detected():
            self.hand = get_biggest_hand(self.hands)
            self.previous_hand_pos = self.hand

    def hand_detected(self):
        if self.hands != ():
            return True
        return False

    def get_hand(self):
        if self.hand_detected():
            return self.hand
        return self.previous_hand_pos


