import common
from utility.image_tools import Camera
import server.map
from server.socket import start_socket
import logging
logger = logging.getLogger(__name__)

from subprocess import run as sp_run
import os
from pathlib import Path

from flask import Flask, render_template, Response, request
import json
import plotly as plt
import numpy as np


b_image = False
b_video = False
video_save_path = None
image_save_path = None

def webpage(app):
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
        count = len(os.listdir(image_save_path))
        file = open(image_save_path+'/img_{:05d}.jpeg'.format(count),'wb') 
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
        sp_run('sudo halt', shell=True)
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
            count = len(os.listdir('{}/videos'.format(video_save_path)))
            os.mkdir('{}/tmp'.format(video_save_path))
            sp_run('nice -n 10 ffmpeg -framerate {2} -i {0}/tmp/img_%05d.jpeg -vf format=yuv420p {0}/mov_{1:03d}.mp4'.format(video_save_path, count, common.config['CAMERA']['framerate']))
            shutil.rmtree('{}videos/tmp'.format(config.save_path))
        b_video = not b_video
        return 'video'
        
    @app.route('/wifi')
    def wifi():
        utility.toggle_wifi()
        
    @app.route('/light')
    def light():
        return 'light'

    @app.route('/save_map')
    def save_map():
        print(request.args.get('a', 0, type=int))
        return 'saved'
        #map.get()
    
def start():
    if common.config.getboolean('SERVER', 'enabled'):
        logger.info('Starting server')
        global image_save_path, video_save_path
        image_save_path = Path(common.config['PATHS']['ImageSavePath'])
        video_save_path = Path(common.config['PATHS']['VideoSavePath'])
        
        app = Flask(__name__, static_folder='static')
        app.host = common.config['SERVER']['ServerIp']
        app.port = common.config['SERVER']['ServerPort']
        app.config['SECRET_KEY'] = 'secret!'
        
        webpage(app)
        socketio = start_socket(app)
        socketio.run(app, debug=False)
    else:
        logger.info('Server disabled')