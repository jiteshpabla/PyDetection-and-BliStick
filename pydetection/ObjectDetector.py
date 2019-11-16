class ODDetectorCommon:

	def setTrainedDataId(self, id = "CASCADE"):
		if id == "CASCADE":
			self.TRAINED_DATA_ID = id
		elif id == "FACE":
			self.TRAINED_DATA_ID = id
		elif id == "HOG":
			self.TRAINED_DATA_ID = id
		else:
			self.TRAINED_DATA_ID = None
			print(id , " is not a valid trained data ID")

	def setTrainedDataLocation(self):
		if self.TRAINED_DATA_ID == None:
			print("Cannot locate trained data location as Trained Data id is not specified")

		else:
			if self.TRAINED_DATA_ID == "CASCADE":
				self.trained_data_location = "trained/haarcascade_default.cascade.xml"	

			elif self.TRAINED_DATA_ID == "FACE":
				self.trained_data_location = "trained/haarcascade_default.cascade.xml"

			elif self.TRAINED_DATA_ID == "HOG":
				self.trained_data_location = "trained/odtrained.hog.xml"

	def getTrainedDataLocation(self):
		return self.trained_data_location

	def getTrainedDataId(self):
		return self.TRAINED_DATA_ID

