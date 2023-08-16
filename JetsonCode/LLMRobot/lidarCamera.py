import numpy as np #importing inside the init function does not work for some reason
import pyrealsense2 as rs
import cv2

class LidarCamera:

    def __init__(self):
        import numpy as np
        import pyrealsense2 as rs
        import cv2
        from PIL import Image 
        self.np = np
        self.rs = rs
        self.Image = Image
        self.depth_image_path = '/home/nesl/JetsonCode/lidarimages/depth_image.png'
        self.color_image_path = '/home/nesl/JetsonCode/lidarimages/color_image.png'


	#------Class Variables----
	#self.depth_array = None
	
    def get_depth_matrix(self):
        # Create a context object. This object owns the handles to all connected realsense devices
        pipeline = self.rs.pipeline()
        pipeline.start()

        try:
            while True:
            # Create a pipeline object. This object configures the streaming camera and owns it's handle
                for i in range(3):
                	frames = pipeline.wait_for_frames()
                frames = pipeline.wait_for_frames()
                depth = frames.get_depth_frame()
                if not depth: 
                    continue
                depth_data = depth.as_frame().get_data()
                np_image = self.np.asanyarray(depth_data)
                np_image = cv2.applyColorMap(cv2.convertScaleAbs(np_image, alpha=0.03), cv2.COLORMAP_JET) #added color overlay
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
                for i in range(3):
                	frames = pipeline.wait_for_frames()
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
        image.save(self.depth_image_path)

    def get_color_image(self):
        image = self.Image.fromarray(self.get_color_matrix())
        image.save(self.color_image_path)
        
    def determine_depth(self, center, upperLeft, upperRight):
        # Create a context object. This object owns the handles to all connected realsense devices
        pipeline = self.rs.pipeline()
        pipeline.start()

        try:
            while True:
            # Create a pipeline object. This object configures the streaming camera and owns it's handle
                for i in range(3):
                    frames = pipeline.wait_for_frames()
                frames = pipeline.wait_for_frames()
                depth = frames.get_depth_frame()
                if not depth:
                    continue
                depth_data = depth.as_frame().get_data()
                np_image = self.np.asanyarray(depth_data)
                np_image = cv2.applyColorMap(cv2.convertScaleAbs(np_image, alpha=0.03), cv2.COLORMAP_JET) #added color overlay
                return np_image
                break
        finally:
            pipeline.stop()
