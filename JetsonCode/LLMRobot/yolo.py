import yolov5

class Yolo:
	depth_image_path = '/home/pragya/lidar_camera/depth_image.jpg'
	color_image_path = '/home/pragya/lidar_camera/color_image.jpg'
	
	# load model
	def __init__(self):
		self.model = yolov5.load('fcakyon/yolov5s-v7.0')
		# set model parameters
		self.model.conf = 0.5  # NMS confidence threshold
		self.model.iou = 0.45  # NMS IoU threshold
		self.model.agnostic = False  # NMS class-agnostic
		self.model.multi_label = False  # NMS multiple labels per box
		self.model.max_det = 500  # maximum number of detections per image

		# img = color_image_path
		#img =  '/home/pragya/Desktop/livingroom.jpg'
		self.img = 'https://github.com/ultralytics/yolov5/raw/master/data/images/zidane.jpg'
		self.data = 0

	#runs the model on an image
	def recognize_obj(self):
		# perform inference
		results = self.model(self.img)
		results.show()
		# inference with larger input size
		results = self.model(self.img, size=640, augment=True)

		# inference with test time augmentation
		#results = self.model(self.img, augment=True)

		# substitute index to object types
		predictions = results.pred[0]
		predictions = predictions.tolist()

		categories = [row[-1] for row in predictions]
		objects_dict = results.names

		for i in range(0, len(predictions)):
			predictions[i][5] = objects_dict[int(categories[i])]
		self.data = predictions 	#save the predictions dictionary as a local attribute of the object 
		return predictions
	
	#searches for a specific object in the last processed image
	def searchObject(self, obj):
		for i in range(0, len(self.data)):
			if self.data[i][5] == obj:
				return True
		return False
		
	#returns a list of indices that refer to a desired object
	def findIndicesForObject(self, obj):
		arr = []
		for i in range(0, len(self.data)):
			if self.data[i][5] == obj:
				arr += [i]
		return arr;
	
	#returns a coordinate/ 2-item array consisting of the x and y values of the center of the box containing the object of a given index
	def findCenter(self, index):
		x = (self.data[index][0] + self.data[index][2])/2
		x = int(x)
		y = (self.data[index][1] + self.data[index][3])/2
		y = int(y)
		arr = [x, y]
		return arr
		
	#Given two object indices, determine whether index 1 is to the left of index 2
	def isLeft(self, index1, index2, direction):
		firstCoord = self.findCenter(index1)
		secondCoord = self.findCenter(index2)
		if direction == "left":	
			return (firstCoord[0] < secondCoord[0])
		if direction == "right":
			return (firstCoord[0] > secondCoord[0])
		if direction == "above":
			return (firstCoord[1] < secondCoord[1])
		if direction == "below":
			return (firstCoord[1] > secondCoord[1])	
			
	#------------------Basic Accessors and Mutators
	def setImage(self, img):
		self.img = img;
