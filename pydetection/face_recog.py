import FaceRecog
import CascadeDetector
import FrameGenerator
import Detection
import cv2
import numpy as np
import cv2
import numpy as np


#import pyttsx
size = 4
fn_haar = 'FACE'
fn_dir = 'database_perfect'


rec = FaceRecog.FaceRecog(recogtype = "OD_LBPH_FACE")
rec.initTrainer(location = fn_dir)
print("Training ......")
image , lables, names, id = rec.train()
#print(names)

(im_width, im_height) = (112, 92)

det = CascadeDetector.CascadeDetector()
det.setTrainedDataId(fn_haar)
det.setTrainedDataLocation()
det.initDetector()

webcam = FrameGenerator.FrameGenerator(0)
#print("ho")
count = 1
while count<45 or cv2.waitKey==13:
    (_, im) = webcam.genNextFrame()
    #time.sleep(0.38)
    cv2.imshow('OpenCV', im)
    count += 1
im = cv2.flip(im, 1, 0)

det.setScaleFactor(1.3)
det.setMinNeighbours(5)

gray = det.gray(im)
faces = det.detect(gray)
print(len(faces))

detection = Detection.Detection2D(scene = im)
for (x,y,w,h) in faces:
    detection.drawBoundingBox(x,y,w,h,2,(255,0,0))
    #cv2.rectangle(im,(x,y),(x+w,y+h),(255,0,0),2)
    face = gray[y:y + h, x:x + w]
    detection.drawBoundingBox(x,y,w,h,3,(0,255,0))
    #cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 3)

    pred, l, conf = rec.predict(face, im_width, im_height)
    print(pred, conf)
    #print (&amp;quot;pred&amp;quot;,prediction)
    if conf < 75:
        #cv2.putText(im,'%s - %.0f' % (names[pred],pred),(x-10, y-10), cv2.FONT_HERSHEY_PLAIN,1,(0, 255, 0))
        detection.putText(text = "%s - %.0f" % (names[pred],conf), font=cv2.FONT_HERSHEY_PLAIN,color = (0,255,0))
    else:
        #cv2.putText(im,'not recognized',(x-10, y-10),cv2.FONT_HERSHEY_PLAIN,1,(0, 0,255))
        detection.putText(text = "not recognized", font=cv2.FONT_HERSHEY_PLAIN,color = (0,0,255))
cv2.imshow('OpenCV', im)
key = cv2.waitKey(10000)

webcam.release()
cv2.destroyAllWindows()
