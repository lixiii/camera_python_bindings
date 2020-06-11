import numpy as np
import timeit
from PIL import Image

import camera_capture

def capture():
    raw_img = camera_capture.capture()
    return np.array(raw_img)

def save(np_array):
    img = Image.fromarray(np_array)
    img.save('image.png')

def capture_and_save():
    a = capture()
    save(a)

if __name__=="__main__":
    print("Timing 10 runs of capture(): ")
    print( timeit.timeit("capture()","from __main__ import capture",number=10) )
    print("Timing 10 runs of capture_and_save(): ")
    print( timeit.timeit("capture_and_save()","from __main__ import capture_and_save",number=10) )
    