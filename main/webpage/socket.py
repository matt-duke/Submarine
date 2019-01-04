import common

from threading import Lock
from flask_socketio import SocketIO, send, emit
from time import time
import logging

thread_lock = Lock()
thread = None
namespace = '/io'

def start_socket(app):
    async_mode = None
    socketio = SocketIO(app, async_mode=async_mode)
    
    def background_thread():
        print('background task')
        rate = common.config.getint('SERVER', 'GuiRefresh')  
        while True:
            socketio.sleep(rate)
            for key, sensor in common.sensors.items():
                socketio.emit('refresh', {'id': key,'data':sensor.__dict__}, namespace = namespace)
                logger.debug("emitting")
            socketio.emit('refresh', {'name':'mode','data':common.mode.name}, namespace = namespace)
            #socketio.emit('test', 'test', namespace=namespace)
    
    @socketio.on('connect', namespace=namespace)
    def connect():
        emit('sensor-list', list(common.sensors.keys()), namespace=namespace)
        global thread
        if thread == None:
            thread = socketio.start_background_task(target = background_thread)

    @socketio.on_error(namespace) # handles the '/chat' namespace
    def error_handler_chat(e):
        print(e)
    
    return socketio