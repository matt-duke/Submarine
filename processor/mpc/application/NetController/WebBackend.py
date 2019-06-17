from flask import Flask

import core
import common

class FlaskApp(core.BaseClass):
    def __init__(self):
        self.app = Flask(__name__)
        self.define_callbacks()
        
        core.BaseClass.__init__(self)
    
    def define_callbacks(self):
        app = self.app
        @app.route("/")
        def hello():
            self.logger.info('Server access')
            return "Hello World!"