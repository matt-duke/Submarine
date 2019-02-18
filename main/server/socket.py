import common

from threading import Lock
from flask_socketio import SocketIO, send, emit
from time import time
import logging

logger = logging.getLogger(__name__)

thread_lock = Lock()
thread = None
namespace = '/io'

def socket(app):
    logger.info('Starting SocketIO')
    async_mode = None
    socketio = SocketIO(app, async_mode=async_mode)
    
    def background_thread():
        logger.info('Background socket stream started')
        rate = common.config.getint('SERVER', 'GuiRefresh')  
        while True:
            for bus in common.bus:
                for key, sensor in bus.items():
                    data = {'value': sensor.value,
                            'valid': sensor.valid
                            }
                    socketio.emit('update', {'id': key,'data':data}, namespace = namespace)
                #socketio.emit('update', {'id':'mode','data':common.mode.name}, namespace = namespace)
            socketio.emit('refresh', namespace=namespace)
            socketio.sleep(rate)
    
    @socketio.on('connect', namespace=namespace)
    def connect():
        logger.info('Client connected')
        sensor_list = common.flatten([list(b.keys()) for b in common.bus])
        emit('sensor-list', sensor_list, namespace=namespace)
        global thread
        if thread == None:
            thread = socketio.start_background_task(target = background_thread)

    @socketio.on_error(namespace)
    def error_handler_chat(e):
        print(e)
    
    return socketio