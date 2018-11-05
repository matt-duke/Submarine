from flask import Flask, render_template, Response
from utility.camera import Camera
from flask_socketio import SocketIO, emit
from threading import Thread
import logging
from time import sleep
import os
import shutil
import utility.map as map

import src.config as config
from src.comm import I2c
from utility.rpi import gpio_init

app = Flask(__name__, template_folder='webpage/templates', static_folder='webpage/static')
socketio = SocketIO(app)

b_image = False
b_video = False

def print_sensor(id, delay=1):
    while True:
        #print(config.sensor[id].value)
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
    msg_map = ['take_photo','start_video', 'stop_video', 'save_map']

    @socketio.on('get_msg_map')
    def handle_send_map():
        print('sending map')
        emit('get_msg_map', msg_map)

    for i in range(len(msg_map)):
        @socketio.on(msg_map[i])
        def msg_handler(message):
            global b_image, b_video
            if config.debug[0]:
                print('received message: ' + message)
            if i == 0:
                b_image = True
            elif i == 1:
                b_video = True
            elif i == 2:
                b_video = False
            elif i == 3:
                b_video = False
                count = len(os.listdir('{}videos'.format(config.save_path)))
                os.system('nice -n 10 ffmpeg -framerate {2} -i {0}videos/tmp/img_%05d.jpeg -vf format=yuv420p {0}videos/mov_{1:03d}.mp4'.format(config.save_path, count, config.cam_settings['framerate']))
                shutil.rmtree('{}videos/tmp'.format(config.save_path))
                os.mkdir('{}videos/tmp'.format(config.save_path))
            elif i == 4:
                print(message)
                

start()
webpage()
socket()
app.run(host='0.0.0.0', debug=config.debug[0])
socketio.run()
