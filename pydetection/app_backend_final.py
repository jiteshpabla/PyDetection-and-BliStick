from flask import Flask,jsonify,make_response,request
import base64
import cv2
import FaceRecog
import CascadeDetector
import FrameGenerator
from PIL import Image
from imutils.object_detection import non_max_suppression
from imutils import paths
import imutils
import numpy as np
import os, sys, time
#import ty
import json

print("Hello")
fn_haar = 'FACE'
fn_dir = 'database'


rec = FaceRecog.FaceRecog(recogtype = "OD_LBPH_FACE")
rec.initTrainer(location = fn_dir)
(image, lables, names, id)=([],[],{},0) 
print("Training ......")
image , lables, names, id = rec.train()

hog = cv2.HOGDescriptor()
hog.setSVMDetector( cv2.HOGDescriptor_getDefaultPeopleDetector() )

app = Flask(__name__)


def pydetect_vid(name):
	size = 4
	fn_haar = 'trained/haarcascade_frontalface_default.xml'
	fn_dir = 'database'
	path = os.path.join(fn_dir, name)
	if not os.path.isdir(path):
		os.mkdir(path)
	(im_width, im_height) = (224, 184)
	haar_cascade = cv2.CascadeClassifier(fn_haar)
	webcam = cv2.VideoCapture(name+".mp4")
	count = 1
	(rval, im) = webcam.read()
	rval = True
	while rval:
		(rval, im) = webcam.read()
		print(rval)
		#im = cv2.flip(im, 1, 0)
		if rval == True:
			gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
			mini = cv2.resize(gray, (int(gray.shape[1]/size), int(gray.shape[0]/size)))
			faces = haar_cascade.detectMultiScale(mini)
			print(len(faces))
			faces = sorted(faces, key=lambda x: x[3])
			if faces:
				face_i = faces[0]
				(x, y, w, h) = [v * size for v in face_i]
				print(x," ",y," ",w," ",h)
				face = gray[y:y + h, x:x + w]
				face_resize = cv2.resize(face, (im_width, im_height))
				pin=sorted([int(n[:n.find('.')]) for n in os.listdir(path) if n[0]!='.' ]+[0])[-1] + 1
				if count%2==1:
					cv2.imwrite('%s/%s.png' % (path, pin), face_resize)
				#time.sleep(0.38)
			#cv2.imwrite('%s/%d.png' %(path,count), )
			cv2.imshow('OpenCV', im)
			#if count == 45:
			#	break
		count = count + 1

	print (str(count) + " images taken and saved to " + name +" folder in database ")



@app.route('/')
def index():
    return "Face Classifier server says hello!"

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/upload',methods=['POST'])
def uploadjson():
	print (request.is_json)
	content=request.get_json()
	print("ayy")
	print (content)
	print(content['base64'])
	return make_response(jsonify({'imageBLOB':content['base64']}),200)

@app.route('/uploadHog',methods=['POST'])
def hogrecog():
	content=request.get_json()
	img_data=content['ImageHog']
	imgdata = base64.b64decode(img_data)
	filename = 'image2.jpg'
	with open(filename, 'wb') as f:
		f.write(imgdata)

	image=cv2.imread('image2.jpg')
	send = 'No'

	(rects, weights) = hog.detectMultiScale(image, winStride=(4, 4),padding=(8, 8), scale=1.05)

	rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
	pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)

	send = str(len(pick))
	print(send)
	send = send + " People Detected"
	data2 = {"name":send}
	return jsonify(data2)


@app.route('/uploadimg',methods=['POST'])
def frecog():
	content=request.get_json()
	img_data=content['ImageBLOB']
	imgdata = base64.b64decode(img_data)
	filename = 'image2.jpg'
	with open(filename, 'wb') as f:
		f.write(imgdata)
	#name=ty.m()
	im = cv2.imread("image2.jpg")
	im = cv2.flip(im, 1, 0)
	size = 4


	#print(names)

	(im_width, im_height) = (224, 184)

	det = CascadeDetector.CascadeDetector()
	det.setTrainedDataId(fn_haar)
	det.setTrainedDataLocation()
	#print(det.getTrainedDataLocation())
	det.initDetector()
	det.setScaleFactor(1.3)
	det.setMinNeighbours(5)

	gray = det.gray(im)
	#cv2.imwrite("gray.jpg",gray)
	print(names)
	faces = det.detect(gray)
	print(len(faces))
	send = ""
	for (x,y,w,h) in faces:
	    cv2.rectangle(im,(x,y),(x+w,y+h),(255,0,0),2)
	    face = gray[y:y + h, x:x + w]
	    cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 3)

	    pred, l, conf = rec.predict(face, im_width, im_height)
	    print(pred, conf)
	    #print (&amp;quot;pred&amp;quot;,prediction)
	    if conf < 80:
	        send = send + names[pred] + " "
	        cv2.putText(im,'%s - %.0f' % (names[pred],pred),(x-10, y-10), cv2.FONT_HERSHEY_PLAIN,1,(0, 255, 0))
	    else:
	        send = send + "Unrecognized face" + " "
	        cv2.putText(im,'not recognized',(x-10, y-10),cv2.FONT_HERSHEY_PLAIN,1,(0, 0,255))
	cv2.imshow('OpenCV', im)
	#key = cv2.waitKey(10000)

	#webcam.release()
	#cv2.destroyAllWindows()
	#server_response = [{'aaa', "lmao"}]
	#josn_obj = demjson.encode(server_response)
	if len(faces) == 0:
		send = "Nothing "
	send = send + "Detected"
	print(send)
	data2 = {"name":send}

	#json_data = json.dumps(data2)
	return jsonify(data2)

@app.route('/uploadvid',methods=['POST'])
def frecog2():
	content=request.get_json()
	vid_data=content['video']
	viddata = base64.b64decode(vid_data)
	person_name = content['name']
	print (person_name)
	filename = person_name+'.mp4'
	with open(filename, 'wb') as f:
    		f.write(viddata)
	#name=ty.m()
	data2 = {"name": "Success"}

	pydetect_vid(person_name)
	print("Training ......")
	image , lables, names, id = rec.train()
	return jsonify(data2)
	#return "aaaaa"


if __name__ == '__main__':
	app.run(host= '0.0.0.0')
