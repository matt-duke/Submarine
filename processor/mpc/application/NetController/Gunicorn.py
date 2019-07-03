from __future__ import unicode_literals

import common
import logging
import multiprocessing
import gunicorn.app.base
from gunicorn import glogging
from gunicorn.six import iteritems


def number_of_workers():
    return (multiprocessing.cpu_count() * 2) + 1

class WSGI(gunicorn.app.base.BaseApplication):

    def __init__(self, app, options=None):
        self.options = options or {}
        if 'workers' not in self.options.keys():
            self.options['workers'] = number_of_workers()
        self.application = app

        super(WSGI, self).__init__()     

    def load_config(self):
        config = dict([(key, value) for key, value in iteritems(self.options)
                       if key in self.cfg.settings and value is not None])
        for key, value in iteritems(config):
            self.cfg.set(key.lower(), value)

    def set_formatter(self):
        rootLog = logging.getLogger()
        errorLog = logging.getLogger("gunicorn.error")
        accessLog = logging.getLogger("gunicorn.access")
    
        for hdlr in errorLog.handlers:
            errorLog.removeHandler(hdlr)
        for hdlr in accessLog.handlers:
            accessLog.removeHandler(hdlr)
        for hdlr in rootLog.handlers:
            accessLog.addHandler(hdlr)
            errorLog.addHandler(hdlr)
        errorLog.setLevel(rootLog.level)
        accessLog.setLevel(rootLog.level)
    
    def load(self):
        return self.application
    
    def run(self):
        #self.set_formatter()
        gunicorn.app.base.BaseApplication.run(self)