#!/usr/bin/env python
import sys, time
from flask import Flask, render_template, Response
from PIL import Image
import io

# emulated camera
from camera import Camera 
cam = Camera()

app = Flask(__name__, template_folder='./')


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen(camera):
    """Video streaming generator function."""
    while True:
        np_array = camera.capture()
        img = Image.fromarray(np_array)
        img = img.resize((round( img.size[0]/4 ), round( img.size[1]/4 )))
        imgByteArr = io.BytesIO()
        img.save(imgByteArr, format='JPEG', quality=40)
        # print(len(frame))
        yield (b'--frame\r\n'
               b'Content-Type: image/png\r\n\r\n' + imgByteArr.getvalue() + b'\r\n')
        time.sleep(0.5)


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(cam),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.before_first_request
def init_camera():
    cam.init()
if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', debug=True, threaded=False)
    except KeyboardInterrupt: 
        print("Gracefully shutting down")
        cam.close()
        sys.exit(0)