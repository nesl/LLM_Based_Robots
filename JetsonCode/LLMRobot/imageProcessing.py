import yolov5

class ImageProcessing:
	depth_image_path = '/home/pragya/lidar_camera/depth_image.jpg'
	color_image_path = '/home/pragya/lidar_camera/color_image.jpg'
    
	def __init__(self):
        #LIDAR CAMERA INITIALIZATION
        import numpy as np
        import pyrealsense2 as rs
        from PIL import Image
        self.np = np
        self.rs = rs
        self.Image = Image
 
        #YOLO INITIALIZATION
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

# ---------------------------------- LIDAR CAMERA BASED ------------------------------------------------

    def get_depth_matrix(self):
        # Create a context object. This object owns the handles to all connected realsense devices
        pipeline = self.rs.pipeline()
        pipeline.start()

        try:
            while True:
            # Create a pipeline object. This object configures the streaming camera and owns it's handle
                frames = pipeline.wait_for_frames()
                depth = frames.get_depth_frame()
                if not depth:
                    continue
                depth_data = depth.as_frame().get_data()
                np_image = self.np.asanyarray(depth_data)
                return np_image
                break
        finally:
            pipeline.stop()

    def get_color_matrix(self):
        pipeline =self.rs.pipeline()
        pipeline.start()

        try:
            while True:
            # Create a pipeline object. This object configures the streaming camera and owns it's handle
                frames = pipeline.wait_for_frames()
                color = frames.get_color_frame()
                if not color:
                    continue
                color_data = color.as_frame().get_data()
                np_image = self.np.asanyarray(color_data)
                return np_image
                break
        finally:
            pipeline.stop()

    def get_depth_image(self):
        image = self.Image.fromarray(self.get_depth_matrix())
        image.save(depth_image_path)

    def get_color_image(self):
        image = self.Image.fromarray(self.get_depth_matrix())
        image.save(color_image_path)

# ---------------------------------- YOLO BASED ------------------------------------------------

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
	
		
		

		
#------------------------------------testing------------------------------
y = Yolo()
print(y.recognize_obj())
print(y.findIndicesForObject('fish'))
print(y.findCenter(1))
print(y.findCenter(2))
print(y.isLeft(1,2))
print(y.isAbove(0, 1))
