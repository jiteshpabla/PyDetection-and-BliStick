import CascadeDetector
from CascadeDetector import CascadeDetector
#from ObjectDetector import ODDetectorCommon
import FrameGenerator
import cv2
import numpy as np


#import pyttsx
size = 4
fn_haar = 'CASCADE'
#fn_dir = 'database'

(im_width, im_height) = (112, 92)

#det2 = ODDetectorCommon(fn_haar)

det = CascadeDetector()
det.setTrainedDataId(fn_haar)
det.setTrainedDataLocation()
det.initDetector()
det.setScaleFactor(1.3)
det.setMinNeighbours(5)

webcam = FrameGenerator.FrameGenerator(0)
#print("ho")

while True:
    (_, im) = webcam.genNextFrame()
    im = cv2.flip(im, 1, 0)

    gray = det.gray(im)
    faces = det.detect(gray)
    #print("face")
    for (x,y,w,h) in faces:
        cv2.rectangle(im,(x,y),(x+w,y+h),(255,0,0),2)
        face = gray[y:y + h, x:x + w]
        face_resize = cv2.resize(face, (im_width, im_height))
        cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 3)
        #print (&amp;quot;pred&amp;quot;,prediction)
    cv2.imshow('OpenCV', im)
    key = cv2.waitKey(10)
    if key == 27:
        break

webcam.release()
cv2.destroyAllWindows()
