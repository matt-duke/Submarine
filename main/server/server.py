import common
from control.image_tools import Camera
from server import Map
import server.socket
import logging
logger = logging.getLogger(__name__)

import subprocess as sp
import os
from pathlib import Path

from flask import Flask, render_template, jsonify, Response, request, send_file
import json
import plotly as plt
import numpy as np
import json


class Server:
    def __init__(self):
        self.image_save_path = Path(common.config.get('PATHS','ImageSavePath'))
        self.video_save_path = Path(common.config['PATHS']['VideoSavePath'])
        self.tile_save_path = Path(common.config['PATHS']['TileSavePath'])
        self.app = Flask(__name__, static_folder='static')  
        self.app.host = 'localhost'
        self.app.port = common.config['SERVER']['ServerPort']
        self.app.config['SECRET_KEY'] = 'secret!'
        self.map = server.Map(self)
        self.setup(self.app)        
    
    def start(self):
        if common.config.getboolean('SERVER', 'enabled'):        
            logger.info('Starting server')
            
            socketio = server.socket(self.app)
            socketio.run(self.app, debug=False)
        else:
            logger.info('Server disabled')
    
    def setup(self, app):
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
            sp.run('sudo halt', shell=True)
            return 'shutdown'
            
        @app.route('/camera')
        def camera():
            self.b_image = not self.b_image
            return 'camera'
            
        @app.route('/video')
        def video():
            if self.b_video:
                self.b_video = False
                count = len(os.listdir('{}/videos'.format(video_save_path)))
                os.mkdir('{}/tmp'.format(video_save_path))
                sp.run('nice -n 10 ffmpeg -framerate {2} -i {0}/tmp/img_%05d.jpeg -vf format=yuv420p {0}/mov_{1:03d}.mp4'.format(video_save_path, count, common.config['CAMERA']['framerate']))
                shutil.rmtree('{}videos/tmp'.format(config.save_path))
            self.b_video = not self.b_video
            return 'video'
            
        @app.route('/wifi')
        def wifi():
            utility.toggle_wifi()
            return 'success'
            
        @app.route('/light')
        def light():
            return 'light'

        @app.route('/save_map')
        def save_map():
            lat = request.args.get('lat', 0, type=float)
            lon = request.args.get('lon', 0, type=float)
            print(self.tile_save_path)
            self.map.get(lat, lon)
            return 'started in thread'
        
        @app.route('/clear_map')
        def clear_map():
            self.map.clear_tiles()
            return 'cleared'
            
        @app.route('/tile/<path:filename>')
        def get_tile(filename):
            filename = Path(filename)
            tile = os.path.join(os.getcwd(), self.tile_save_path, filename)
            print(tile)
            if os.path.exists(tile):
                return send_file(tile)
            else:
                return send_file(os.path.join(os.getcwd(), self.tile_save_path, 'not_found.png'))
        
        @app.route('/gallery')
        def gallery():
            with open('server/static/image_metadata.json') as f:
                image_metadata = json.load(f)
            
            data = []
            for pg in image_metadata['photoGroups']:
                data.append({'lat':pg['lat'], 'lon':pg['lon']})
                
                title=[]
                footer=[]
                images=[]
                for p in pg['photos']:
                    images.append('media'+p['path'])
                    filename = os.path.basename(p['path'])
                    title.append("<b>{}</b>".format(filename))
                    footer.append("{}, {}<br>{}: {}".format(p['lat'], p['lon'], p['date'], p['time']))
                data[-1]['popup'] = render_template("gallery.html", images=images, footer=footer, title=title, id=pg['lat']+pg['lon'])
            return jsonify(data)