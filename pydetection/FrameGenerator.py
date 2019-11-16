import cv2
import numpy as np

class FrameGenerator:

	def __init__(self, inpt = 0):
		self.cap  = cv2.VideoCapture(inpt)
		if self.cap.isOpened() == False:
			print( "FATAL: Cannot open video capture!")

	def __init__(self, inpt = ""):
		self.cap  = cv2.VideoCapture(inpt)
		if self.cap.isOpened() == False:
			print( "FATAL: Cannot open video capture!")

	def isValid(self):
		return self.cap.isOpened()


	def genNextFrame(self):
		(_, im) = self.cap.read()
		return (_, im)

	def release(self):
		self.cap.release()