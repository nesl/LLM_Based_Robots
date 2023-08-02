class ImageProcessing:

    def __init__(self):
        from .lidarCamera import LidarCamera
        from .yolo import Yolo
        self.LidarCamera = LidarCamera()
        self.Yolo = Yolo()
    
    #------ For LiDar camera -----
    def get_depth_matrix(self):
        return self.LidarCamera.get_depth_matrix()

    def get_color_matrix(self):
        return self.LidarCamera.get_color_matrix()

    def get_depth_image(self):
        return self.LidarCamera.get_depth_image()

    def get_color_image(self):
        return self.LidarCamera.get_color_image()
        
    #----- For Yolo model -----
    #runs the model on an image
    def recognize_Objects(self):
        return self.Yolo.recognize_obj()
    
    #searches for a specific object in the last processed image
    def search_For_Object(self, obj):
        return self.Yolo.searchObject(obj)
        
    #returns a list of indices that refer to a desired object
    def find_Indices_For_Object(self, obj):
        return self.Yolo.findIndicesForObject(obj)
    
    #returns a coordinate/ 2-item array consisting of the x and y values of the center of the box containing the object of a given index
    def find_Center_of_Object(self, index):
        return self.Yolo.findCenter(index)
        
    #Given two object indices, compare locations
    def determine_Relative_Location(self, index1, index2, direction):
        return self.Yolo.isLocation(index1, index2, direction)
        
        
    #----- Fusion Functions -----
    def listAllObjects(self):
    	self.get_color_image()
    	self.recognize_Objects()
    	objectDictionary = self.Yolo.listAllObjects()
    	
    	for item in objectDictionary:
    		amount = objectDictionary[item]
    		print(f"There are {amount} {item}s.")
    	
    
    def findObject(self, obj):
    	self.get_color_image()
    	self.recognize_Objects()
    	if self.search_For_Object(obj) == False: return False
    	
    	
            
    #------------------Basic Accessors and Mutators
    def setImage(self, img):
        self.img = img;
