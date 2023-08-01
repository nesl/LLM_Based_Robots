import yolov5

class ImageProcessing:
    depth_image_path = '/home/pragya/lidar_camera/depth_image.jpg'
    color_image_path = '/home/pragya/lidar_camera/color_image.jpg'

    def __init__(self):
        #LIDAR PORTION
        import numpy as np
        import pyrealsense2 as rs
        from PIL import Image 
        self.np = np
        self.rs = rs
        self.Image = Image
        
        #YOLO PORTION
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
