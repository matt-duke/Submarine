import common
import core

from multiprocessing import Process, Pipe

import logging

from . import WSGI, FlaskApp

class NetController(core.BaseClass):
    def __init__(self):
        core.BaseClass.__init__(self)
        
        self.Flask = FlaskApp()
        
        options = {'bind': 'unix:/tmp/gunicorn.sock'}
        self.wsgi = WSGI(self.Flask.app, options)
       
    def start(self):
        #thread = self.threads.add('gunicorn_wsgi', self.wsgi.run, args=(self.wsgi,))
        #thread.start()
        p = Process(target=self.wsgi.run)
        p.start()