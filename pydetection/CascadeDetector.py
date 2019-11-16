import cv2
import sys, os, time
import ObjectDetector
from ObjectDetector import ODDetectorCommon


class CascadeDetector(ODDetectorCommon):

	def __init__(self, id=None, scaleFactor = 1.1, minNeighbours = 3):
		self.scaleFactor = scaleFactor
		self.minNeighbours = minNeighbours
		#self.minSize = cv2.Size()
		#self.maxSize = cv2.Size()
		self.detector = None

	def setScaleFactor(self, scaleFactor):
		self.scaleFactor = scaleFactor

	def getScaleFactor(self):
		return self.scaleFactor

	
	def setMinNeighbours(self, neighbour):
		self.minNeighbours = neighbour

	def getMinNeighbours(self):
		return self.minNeighbours


	def initDetector(self):
		if self.trained_data_location == None:
			print("No training data location specified")
			return None
		self.detector = cv2.CascadeClassifier(self.trained_data_location)
	
	def detect(self, scene):
		faces = self.detector.detectMultiScale(scene, self.scaleFactor, self.minNeighbours)
		return faces

	def gray(self, scene):
		gray = cv2.cvtColor(scene, cv2.COLOR_BGR2GRAY)
		return gray
'''
if __name__ == '__main__':
	det = CascadeDetector('CASCADE')
	det.setTrainedDataId()
	print(det.getTrainedDataId())
'''