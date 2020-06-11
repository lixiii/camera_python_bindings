import numpy as np
import timeit
from PIL import Image

import camera

def capture(hCamera:int):
    raw_img = camera.capture(hCamera)
    return np.array(raw_img)

def save(np_array):
    img = Image.fromarray(np_array)
    img.save('image.png')

def capture_and_save(hCamera:int):
    a = capture(hCamera)
    save(a)

if __name__=="__main__":
    hCamera:int = camera.init()
    print("Timing 10 runs of capture(): ")
    print( timeit.timeit(f"capture({hCamera})","from __main__ import capture",number=10) )
    print("Timing 10 runs of capture_and_save(): ")
    print( timeit.timeit(f"capture_and_save({hCamera})","from __main__ import capture_and_save",number=10) )
    