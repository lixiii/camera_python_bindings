import numpy as np
from PIL import Image

import camera

cam = camera.init()
raw_img = camera.capture(cam)
np_array = np.array(raw_img)

print(np_array.shape)

img = Image.fromarray(np_array)
img.save('image.png')