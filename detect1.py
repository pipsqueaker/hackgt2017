from __future__ import print_function


"""
'''
example to detect upright people in images using HOG features
Usage:
    peopledetect.py <image_names>
Press any key to continue, ESC to stop.
'''
"""
import time
import numpy as np
import cv2
import cv

# https://github.com/opencv/opencv/blob/master/samples/python/peopledetect.py
def inside(r, q):
    rx, ry, rw, rh = r
    qx, qy, qw, qh = q
    return rx > qx and ry > qy and rx + rw < qx + qw and ry + rh < qy + qh


def draw_detections(img, rects, thickness = 1):
    for x, y, w, h in rects:
        # the HOG detector returns slightly larger rectangles than the real objects.
        # so we slightly shrink the rectangles to get a nicer output.
        pad_w, pad_h = int(0.15*w), int(0.05*h)
        cv2.rectangle(img, (x+pad_w, y+pad_h), (x+w-pad_w, y+h-pad_h), (0, 255, 0), thickness)


if __name__ == '__main__':
    import sys
    from glob import glob
    import itertools as it

    print(__doc__)

    hog = cv2.HOGDescriptor()
    hog.setSVMDetector( cv2.HOGDescriptor_getDefaultPeopleDetector() )

    cascade = cv2.CascadeClassifier()
    cascade.load("Head/haarcascade_upperbody.xml")


    default = ['../data/basketball2.png '] if len(sys.argv[1:]) == 0 else []

    fgbg = cv2.BackgroundSubtractorMOG2()

    vid = cv2.VideoCapture()
    vid.open("vidstab.mp4")

    while vid.isOpened():
        (status, frame) = vid.read()
        frame = cv2.resize(frame, (0,0), fx=.3, fy=.3)
#	frame_masked = fgbg.apply(frame)
        found = hog.detectMultiScale(frame, minNeighbors=2, minSize=(50,50), maxSize = (200, 200))
        #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        found_filtered = []
        for ri, r in enumerate(found):
            for qi, q in enumerate(found):
                if ri != qi and inside(r, q):
                    break
                else:
                    found_filtered.append(r)
        draw_detections(frame, found)
        draw_detections(frame, found_filtered, 3)
        print('%d (%d) found' % (len(found_filtered), len(found)))
        cv2.imshow('img', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            exit()

vid.release()