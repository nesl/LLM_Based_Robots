class LidarCamera:

    def __init__(self):
        import numpy as np
        import pyrealsense2 as rs
        from PIL import Image 
        self.np = np
        self.rs = rs
        self.Image = Image
        self.depth_image_path = '/home/lidarimages/depth_image.jpg'
        self.color_image_path = '/home/lidarimages/color_image.jpg'

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
        image.save(self.depth_image_path)

    def get_color_image(self):
        image = self.Image.fromarray(self.get_color_matrix())
        image.save(self.color_image_path)
