from flask import Flask, render_template, Response
from webpage.camera import Camera
from flask_socketio import SocketIO
from threading import Thread
import logging
from time import sleep

import src.config as config
from src.comm import I2c
from utility.rpi import gpio_init

app = Flask(__name__)
#socketio = SocketIO(app)

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
    threads.append(Thread(target=print_sensor, args=(0,3)))
    for t in threads:
        t.setDaemon(True)
        t.start()

def webpage():       
    @app.route('/')
    def index():
        return render_template('index.html')

    def gen(camera):
        while True:
            frame = camera.get_frame()
            yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    @app.route('/video_feed')
    def video_feed():
        return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

start()
webpage()
app.run(host='0.0.0.0', debug=True)
#socketio.run()
