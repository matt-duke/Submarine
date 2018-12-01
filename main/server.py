from flask import Flask, render_template, Response, request
from utility.camera import Camera

from flask_socketio import SocketIO, emit
from subprocess import call
from time import sleep
import os

import json
import plotly as plt
import numpy as np


app = Flask(__name__, template_folder='webpage/templates', static_folder='webpage/static')
socketio = SocketIO(app)

b_image = False
b_video = False


def stream():
    def save_frame(frame):
        global b_image, b_video
        add_to_path = ''
        if b_image:
            add_to_path = 'images'
            b_image = False
        elif b_video:
            add_to_path = 'videos/tmp'
        else:
            return
        path = config.save_path+add_to_path
        count = len(os.listdir(path))
        file = open(path+'/img_{:05d}.jpeg'.format(count),'wb') 
        file.write(bytearray(frame))
        file.close()

    @app.route('/')
    def index():
        count = 500
        xScale = np.linspace(0, 100, count)
        yScale = np.random.randn(count)
 
        # Create a trace
        trace = plt.graph_objs.Scatter(
            x = xScale,
            y = yScale
        )
 
        data = [trace]
        graphJSON = json.dumps(data, cls=plt.utils.PlotlyJSONEncoder)
        return render_template('index.html', graphJSON=graphJSON)

    def gen(Camera):
        while True:
            frame = Camera.get_frame()
            save_frame(frame)
            yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    @app.route('/video_feed')
    def video_feed():
        return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/shutdown')
def shutdown():
    sleep(5)
    call('sudo halt', shell=True)
    return 'shutdown'
    
@app.route('/camera')
def camera():
    global b_image
    b_image = not b_image
    return 'camera'
    
@app.route('/video')
def video():
    global b_video
    if b_video:
        b_video = False
        count = len(os.listdir('{}videos'.format(config.save_path)))
        os.system('nice -n 10 ffmpeg -framerate {2} -i {0}videos/tmp/img_%05d.jpeg -vf format=yuv420p {0}videos/mov_{1:03d}.mp4'.format(config.save_path, count, config.cam_settings['framerate']))
        shutil.rmtree('{}videos/tmp'.format(config.save_path))
        os.mkdir('{}videos/tmp'.format(config.save_path))
    b_video = not b_video
    return 'video'
    
@app.route('/wifi')
def wifi():
    if call('ifconfig | grep -c wlan', shell=True):
        call('rfkill block wifi', shell=True)
    else:
        call('rfkill unblock wifi', shell=True)
    return 'wifi'
    
@app.route('/light')
def light():
    return 'light'
                    
def socket():
    msg_map = []

    @socketio.on('get_msg_map')
    def handle_send_map():
        print('sending map')
        emit('get_msg_map', msg_map)
    
    for i in range(len(msg_map)):
        @socketio.on(msg_map[i])
        def msg_handler(message):
            pass


    
def start_server():
    stream()
    socket()
    app.run(host='0.0.0.0', debug=config.debug[0])
    socketio.run()
    
if __name__ == '__main__':
    import src.config as config
    config.init()
    start_server()
