class ImageProcessing2:

    def __init__(self):
        import LidarCamera
        import Yolo
        self.LidarCamera = LidarCamera
        self.Yolo = Yolo
    
    #------ For LiDar camera -----
    def get_depth_matrix(self):
        return LidarCamera.get_depth_matrix()

    def get_color_matrix(self):
        return LidarCamera.get_color_matrix()

    def get_depth_image(self):
        return LidarCamera.get_depth_image()

    def get_color_image(self):
        return LidarCamera.get_color_image()
        
    #----- For Yolo model -----
    #runs the model on an image
    def recognize_obj(self):
        return Yolo.recognize_obj()
    
    #searches for a specific object in the last processed image
    def searchObject(self, obj):
        return Yolo.searchObject(obj)
        
    #returns a list of indices that refer to a desired object
    def findIndicesForObject(self, obj):
        return Yolo.findIndicesForObject(obj)
    
    #returns a coordinate/ 2-item array consisting of the x and y values of the center of the box containing the object of a given index
    def findCenter(self, index):
        return Yolo.findCenter(index)
        
    #Given two object indices, compare locations
    def isLocation(self, index1, index2, direction):
        return Yolo.isLocation(index1, index2, direction)
            
    #------------------Basic Accessors and Mutators
    def setImage(self, img):
        self.img = img;

