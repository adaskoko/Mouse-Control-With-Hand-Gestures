from detection import action_detection as ad
from observers import action_observer as ao
from observers import camera_observer as co
from observers import photo_taker_observer as pto
from observers import video_saver_observer as vso
import cv2
import time


def main():
    # cap = cv2.VideoCapture('videos/6.avi')

    cap = cv2.VideoCapture(0)
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))

    action_detector = ad.ActionDetector()
    obs = ao.ActionObserver()
    cam = co.CameraObserver()
    # photo = pto.PhotoTakerObserver()
    # vid = vso.VideoSaverObserver(frame_width, frame_height)
    action_detector.attach(obs)
    action_detector.attach(cam)
    # action_detector.attach(photo)
    # action_detector.attach(vid)

    while True:
        start_time = time.time()
        _, frame = cap.read()

        action_detector.detect_action(frame)
        action_detector.notify()

        k = cv2.waitKey(10) & 0xff
        if k == 27:
            break
        print("FPS: ", 1.0 / (time.time() - start_time))


if __name__ == '__main__':
    main()
