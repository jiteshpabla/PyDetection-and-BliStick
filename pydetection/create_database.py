# create_database.py
import CascadeDetector
import FaceRecog
import FrameGenerator
import cv2, sys, numpy, os, time
count = 0
size = 4
fn_haar = 'FACE'
fn_dir = 'database_perfect'
fn_name = sys.argv[1]   #name of the person
path = os.path.join(fn_dir, fn_name)
if not os.path.isdir(path):
    os.mkdir(path)


#(im_width, im_height) = (112, 92)
(im_width, im_height) = (224, 184)
#(im_width, im_height) = (448, 368)

det = CascadeDetector.CascadeDetector()
det.setTrainedDataId(fn_haar)
det.setTrainedDataLocation()
det.initDetector()

webcam = FrameGenerator.FrameGenerator(0)

print ("-----------------------Taking pictures----------------------")
print ("--------------------Give some expressions---------------------")
# The program loops until it has 20 images of the face.

while count < 45:
    (rval, im) = webcam.genNextFrame()
    im = cv2.flip(im, 1, 0)
    gray = det.gray(im)
    mini = cv2.resize(gray, (int(gray.shape[1]/size), int(gray.shape[0]/size)))
    faces = det.detect(mini)
    faces = sorted(faces, key=lambda x: x[3])
    if faces:
        face_i = faces[0]
        (x, y, w, h) = [v * size for v in face_i]
        face = gray[y:y + h, x:x + w]
        face_resize = cv2.resize(face, (im_width, im_height))
        pin=sorted([int(n[:n.find('.')]) for n in os.listdir(path) if n[0]!='.' ]+[0])[-1] + 1
        cv2.imwrite('%s/%s.png' % (path, pin), face_resize)
        cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 3)
        cv2.putText(im, fn_name, (x - 10, y - 10), cv2.FONT_HERSHEY_PLAIN,1,(0, 255, 0))
        #time.sleep(0.38)        
        count += 1
   
    	
    cv2.imshow('OpenCV', im)
    key = cv2.waitKey(10)
    if key == 27:
        break
print (str(count) + " images taken and saved to " + fn_name +" folder in database ")


