import numpy as np
from PIL import Image

from camera import Camera

cam = Camera()
cam.init()
np_array = cam.capture()

print(np_array.shape)

img = Image.fromarray(np_array)
img.save('image.png')
cam.close()