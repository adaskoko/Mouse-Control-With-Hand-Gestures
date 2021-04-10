from observers.observer_dp import Observer
from detection import action_detection as ad
import cv2
import settings

ACTIONS = settings.Gesture.ACTIONS


class CameraObserver(Observer):
    def update(self, subject: ad.ActionDetector) -> None:
        frame = subject.frame.copy()
        if subject.hand is not None:
            (x, y, w, h) = subject.hand
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255), 2)
        else:
            (x, y, w, h) = subject.previous_hand
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255), 2)

        if subject.gesture_area is not None:
            (x, y, w, h) = subject.gesture_area
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
            _, width = frame.shape[:2]
            frame = cv2.flip(frame, 1)
            cv2.putText(frame, 'gesture: ' + ACTIONS[subject.gesture], (width - x - w, y + 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 255))
        else:
            frame = cv2.flip(frame, 1)

        cv2.imshow('Detected gesture', frame)
