import cv2
class Detection2D:

	def __init__(self, scene = None):
		self.scene = scene
		self.boxcolor = (0,0,0)
		self.boxwidth = 2
		self.dim = (0,0,0,0)

	def setBoxColor(self, color):
		self.boxcolor = color

	def setBoxWidth(self, width):
		self.boxwidth = width

	def setDim(self, x, y, w, h):
		self.dim = (x,y,w,h)


	def drawBoundingBox(self, x, y, w, h, thick=None, color=None):
		if thick !=None:
			self.setBoxWidth(thick)
		if color !=None:
			self.setBoxColor(color)
		self.setDim(x,y,w,h)
		cv2.rectangle(self.scene, (self.dim[0], self.dim[1]), (self.dim[0]+self.dim[2], self.dim[1]+self.dim[3]), self.boxcolor, self.boxwidth)

	def putText(self, text="", font="" , color = (0,0,0)):
		 cv2.putText(self.scene,text,(self.dim[0]-10, self.dim[1]-10),font,1,color)

