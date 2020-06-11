import numpy as np
import timeit
import time
from PIL import Image

from camera import Camera
cam = Camera()

def capture():
    raw_img = cam.capture()
    return np.array(raw_img)

def save(np_array):
    img = Image.fromarray(np_array)
    img.save('image.png')

def capture_and_save():
    a = cam.capture()
    save(a)

if __name__=="__main__":
    cam.init()
    print("Timing 10 runs of capture(): ")
    print( timeit.timeit(f"capture()","from __main__ import capture",number=10) )
    print("Timing 10 runs of capture_and_save(): ")
    print( timeit.timeit(f"capture_and_save()","from __main__ import capture_and_save",number=10) )
    cam.close()