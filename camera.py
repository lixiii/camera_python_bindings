import _camera
import numpy as np 
from PIL import Image

class Camera: 
    def __init__(self):
        self._initialised = False

    def init(self):
        if self._initialised==False:
            self.cameraID = _camera.init() 
            self._initialised = True
            self.exposure = self.getExposure()
    
    def capture(self):
        if self._initialised:
            raw_img = _camera.capture(self.cameraID)
            return np.array(raw_img, copy=False)
        else: 
            return False 

    def save(self, path:str):
        a = self.capture()
        img = Image.fromarray(a)
        img.save(path)
    
    def close(self):
        if self._initialised:
            _camera.close(self.cameraID)

    def getExposure(self):
        return _camera.getAETarget( self.cameraID )

    def setExposure( self, target:int ):
        status = _camera.setAETarget( self.cameraID, target )
        self.exposure = self.getExposure()
        return(self.exposure)