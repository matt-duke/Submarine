from flask import Flask
from flask_socketio import SocketIO
from config import *

#import utility
sensor[1].value = 3
def site():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret!'
    socketio = SocketIO(app)

    @app.route("/")
    def index():
        return "Homepage"

    @socketio.on('message')
    def handle_message(message):
        print('received message: ' + message)
    #app.debug = False #https://stackoverflow.com/questions/31264826/start-a-flask-application-in-separate-thread
    app.run()
    socketio.run()