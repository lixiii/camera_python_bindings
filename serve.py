#!/usr/bin/env python
import sys, time
from flask import Flask, render_template, Response, request, redirect, send_file
from PIL import Image, ImageDraw
import io

# emulated camera
from camera import Camera 
cam = Camera()

app = Flask(__name__, template_folder='./')


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html', exposure=cam.exposure, guides = ( request.args.get("guides") ) )


def gen(camera, guides:bool=False):
    """Video streaming generator function."""
    while True:
        np_array = camera.capture()
        img = Image.fromarray(np_array)
        if guides:
            draw = ImageDraw.Draw(img)
            draw.line((round(img.size[0]/2), 0, round(img.size[0]/2), img.size[1]), width=3, fill=(255,100,100))
            draw.line((0, round(img.size[1]/2), img.size[0], round(img.size[1]/2)), width=3, fill=(255,100,100))
        # img = img.resize((round( img.size[0]/4 ), round( img.size[1]/4 )))
        imgByteArr = io.BytesIO()
        img.save(imgByteArr, format='JPEG', quality=50)
        # print(len(frame))
        yield (b'--frame\r\n'
               b'Content-Type: image/png\r\n\r\n' + imgByteArr.getvalue() + b'\r\n')
        time.sleep(0.1)


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    if request.args.get("guides"):
        guides = True
    else: 
        guides = False
    return Response(gen(cam, guides),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/set_exposure")
def set_exposure():
    cam.setExposure( int( request.args["exposure"] ) )
    return redirect("/")

@app.route("/download")
def download():
    a = cam.capture() 
    img = Image.fromarray(a)
    img.save("/home/pi/python_camera/image.png")
    return send_file( "image.png",
        mimetype='image/png',
        as_attachment=True) 
        # attachment_filename="img.jpg")
    

@app.before_first_request
def init_camera():
    cam.init()

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', debug=True, threaded=True)
    except KeyboardInterrupt: 
        print("Gracefully shutting down")
        cam.close()
        sys.exit(0)