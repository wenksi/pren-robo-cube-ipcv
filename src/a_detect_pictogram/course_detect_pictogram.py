import cv2
import pyttsx3
import logging
import time

from src.common.camera.camera import Camera

logging.basicConfig(level=logging.INFO)

path_to_cascades = "../../resources/cascades/pictogram/"
paths = ['hammer.xml', 'sandwich.xml', 'rule.xml', 'paint.xml', 'pencil.xml']  # PATH OF THE CASCADE
objectNames = ['hammer', 'sandwich', 'rule', 'paint', 'pencil']  # OBJECT NAMES TO DISPLAY
objectCount = 21  # how many objects to count for recognition


class PictogramDetector:
    """
    Class loads cascade files, analyzes the video stream and detects pictograms in front of the camera.
    """

    def __init__(self):
        self.camera = Camera()
        self.cascades = []
        for c in paths:  # LOAD THE CLASSIFIERS
            self.cascades.append(cv2.CascadeClassifier(path_to_cascades + c))

        logging.info("Ready for detection")

    def detect(self):
        """
        Used to detect and count pictograms.
        :return: statistics of detected pictograms
        """
        time.sleep(1)
        counter = 0
        stats = {'hammer': 0, 'sandwich': 0, 'rule': 0, 'paint': 0, 'pencil': 0}

        while counter < objectCount:
            image = self.camera.snapshot()
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            work = gray
            for c in self.cascades:
                objects = c.detectMultiScale(work, 1.15, 3)
                for (x, y, w, h) in objects:
                    area = w * h
                    if area > 400:
                        o = objectNames[self.cascades.index(c)]
                        counter += 1
                        stats[o] += 1
                        logging.debug(o)
        return stats


def run():
    """
    Runs the PictogramDetector.
    :return: the pictogram which had the most hits.
    """
    detector = PictogramDetector()
    stats = detector.detect()
    logging.debug(stats)
    result = max(stats, key=stats.get)

    t2s = pyttsx3.init()
    t2s.setProperty('voice', t2s.getProperty('voices'))
    comb = 'some' if result is 'paint' else 'a'
    t2s.say("I am looking for %s %s" % (comb, result))
    logging.info("detected: %s", result)
    t2s.runAndWait()
    return result


if __name__ == '__main__':
    run()