import cv2
import numpy as np

class ODScene():

	path_ = ""

	def getData():
		return

	def getPath():
		return path_

	
class ODSceneImage(ODScene):


	def __init__(self, cvimage, path = ""):
		# np array instead of cv::mat
		self.cvimage_ = np.array()
		self.cvimage_ = cvimage
		self.path_ = path
		# list instead of vector
		self.keypoints_ = []
		self.descriptors_ = np.array()
		self.is_trained_ = False

	def getKeypoints(self):
		return self.keypoints_

	def setKeypoints(kps_):
		self.keypoints_ = kps_


	def getDescriptors(self):
		return self.descriptors_

	def setDescriptors(des_):
		self.descriptors_ = des_

	
	def getCVImage(self):
		return self.cvimage_