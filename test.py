import numpy as np
from PIL import Image

import camera_capture

raw_img = camera_capture.capture()
np_array = np.array(raw_img)

print(np_array.shape)

img = Image.fromarray(np_array)
img.save('image.png')