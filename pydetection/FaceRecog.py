import cv2
import numpy as np
import os, sys, time


class FaceRecog:

	def __init__(self,threshold = 0.0, width = 0, height = 0, recogtype = "OD_EIGEN_FACE"):
		self.threshold = threshold
		self.trainedlocation = None
		self.width = width
		self.height = height
		print(recogtype)
		if recogtype == "OD_EIGEN_FACE":
			self.recognizer = cv2.face.createEigenFaceRecognizer()
		elif recogtype == "OD_LBPH_FACE":
			self.recognizer = cv2.face.createLBPHFaceRecognizer()
		elif recogtype == "OD_FISHER_FACE":
			self.recognizer = cv2.face.createFisherFaceRecognizer()
		else :
			self.recognizer = None
			print(recogtype," is not a valid Face Recognizer ")

	def initTrainer(self, location = None):
		if location is None:
			print("No input Location Specified")
		else:
			self.trainedlocation = location

	def getTrainedDataLocation(self):
		return self.trainedlocation

	#def initDetector();
	def train(self, location = None):
		if self.trainedlocation is None:
			if location is None:
				print("No input location Specified")
			else:
				self.trainedlocation = location
		
		trainedlocation = self.trainedlocation
		#print(trainedlocation)

		(images, lables, names, id) = ([], [], {}, 0)
		for (subdirs, dirs, files) in os.walk(trainedlocation):
			for subdir in dirs:
				names[id] = subdir
				#print(subdir)
				subjectpath = os.path.join(trainedlocation, subdir)
				for filename in os.listdir(subjectpath):
					path = subjectpath + '/' + filename
					lable = id
					images.append(cv2.imread(path, 0))
					lables.append(int(lable))
				id += 1
		
		(images, lables) = [np.array(lis) for lis in [images, lables]]
		#print(lables)
		self.recognizer.train(images, lables)
		return images, lables, names, id

	
	def predict(self, face, im_width , im_height):
		face_resize = cv2.resize(face, (im_width, im_height))
		pred = self.recognizer.predict(face_resize)
		prediction = cv2.face.MinDistancePredictCollector()
		self.recognizer.predict(face_resize,prediction)
		return pred, prediction.getLabel(), prediction.getDist()



	def getRecogType(self):
		return self.recognizer

	def setRecognizer(self, recogtype):
		if recogtype == "OD_EIGEN_FACE":
			self.recognizer = cv2.face.createEigenFaceRecognizer(threshold = float(self.threshold))
		if recogtype == "OD_LBPH_FACE":
			self.recognizer = cv2.face.createLBPHFaceRecognizer(threshold = float(self.threshold))
		if recogtype == "OD_FISHER_FACE":
			self.recognizer = cv2.face.createFisherFaceRecognizer(threshold = float(self.threshold))
		else :
			print(recogtype," is not a valid Face Recognizer ")

	def getThreshold(self):
		return self.threshold

	def setThreshold(self,threshold):
		self.threshold = threshold
