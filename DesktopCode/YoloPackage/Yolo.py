import yolov5

class Yolo:
	depth_image_path = '/home/pragya/lidar_camera/depth_image.jpg'
	color_image_path = '/home/pragya/lidar_camera/color_image.jpg'
	
	# load model
	def __init__(self):
		model = yolov5.load('fcakyon/yolov5s-v7.0')
			
		# set model parameters
		model.conf = 0.5  # NMS confidence threshold
		model.iou = 0.45  # NMS IoU threshold
		model.agnostic = False  # NMS class-agnostic
		model.multi_label = False  # NMS multiple labels per box
		model.max_det = 500  # maximum number of detections per image

		# img = color_image_path
		img =  '/home/pragya/Desktop/livingroom.jpg'

	def recognize_obj(self):
		# perform inference
		results = model(self.img)

		# inference with larger input size
		results = model(self.img, size=640)

		# inference with test time augmentation
		results = model(self.img, augment=True)

		# substitute index to object types
		predictions = results.pred[0]
		predictions = predictions.tolist()

		categories = [row[-1] for row in predictions]
		objects_dict = results.names

		for i in range(0, len(predictions)):
			predictions[i][5] = objects_dict[int(categories[i])]
			
		return predictions

