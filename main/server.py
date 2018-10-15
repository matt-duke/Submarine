from flask import Flask, render_template, Response
from utility.camera import Camera
from flask_socketio import SocketIO
from threading import Thread
import logging
from time import sleep
import os
import shutil

import src.config as config
from src.comm import I2c
from utility.rpi import gpio_init

app = Flask(__name__, template_folder='webpage/templates', static_folder='webpage/static')
socketio = SocketIO(app)

b_image = False
b_video = False

def print_sensor(id, delay=1):
    while True:
        print(config.sensor[id].value)
        sleep(delay)
        
def start():
    config.init()
    config.init_db()
    gpio_init()
    
    mcu = I2c()
    threads = []
    threads.append(Thread(target=mcu.connect))
    threads.append(Thread(target=print_sensor, args=(0,20)))
    #threads.append(Thread(target=cam_test))
    for t in threads:
        t.setDaemon(True)
        t.start()

def webpage():
    #global b_image, b_video
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
        return render_template('index.html')

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

def socket():
    #global b_image, b_video
    @socketio.on('take_photo')
    def handle_take_photo(message):
        global b_image
        print('received message: ' + message)
        b_image = True
        
    @socketio.on('start_video')
    def handle_start_video(message):
        global b_video
        print('received message: ' + message)
        
        b_video = True
        
    @socketio.on('stop_video')
    def handle_stop_video(message):
        global b_video
        print('received message: ' + message)
        b_video = False
        count = len(os.listdir('{}videos'.format(config.save_path)))
        os.system('ffmpeg -framerate {2} -i {0}videos/tmp/img_%05d.jpeg -vf format=yuv420p {0}videos/mov_{1:03d}.mp4'.format(config.save_path, count, config.cam_settings['framerate']))
        shutil.rmtree('{}videos/tmp'.format(config.save_path))
        os.mkdir('{}videos/tmp'.format(config.save_path))
    
start()
webpage()
socket()
app.run(host='0.0.0.0', debug=config.debug[0])
socketio.run()
