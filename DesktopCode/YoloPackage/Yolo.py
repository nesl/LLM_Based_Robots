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

		# inference with larger input size
		results = self.model(self.img, size=640)

		# inference with test time augmentation
		results = self.model(self.img, augment=True)

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


		
#------------------------------------testing------------------------------
y = Yolo()
print(y.recognize_obj())
print(y.searchObject('fish'))
