import _camera
import numpy as np 

class Camera: 
    def __init__(self):
        self._initialised = False

    def init(self):
        if self._initialised==False:
            self.cameraID = _camera.init() 
            self._initialised = True
    
    def capture(self):
        if self._initialised:
            raw_img = _camera.capture(self.cameraID)
            return np.array(raw_img)
        else: 
            return False 
    
    def close(self):
        if self._initialised:
            _camera.close(self.cameraID)

    