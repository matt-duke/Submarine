from pathlib import Path
import os
from os.path import join

class Paths(dict):
    def __init__(self, platform):
        dict.__init__(self)
        
        root = os.getcwd()
        self['ROOT'] = str(Path(root))
        self['CONFIG'] = str(Path(join(root,'configuration','config.ini')))
        self['CONFIG_SCHEMA'] = str(Path(join(root,'configuration','schema.ini')))
        
        if platform == 'Linux':
            self['DEBUG_LOG'] = str(Path('/var/debug.log'))
            self['DATABASE'] = str(Path('/media/data.db'))
            
        elif platform == 'Windows':
            self['DEBUG_LOG'] = str(Path(join(root, 'debug.log')))
            self['DATABASE'] = str(Path(join(root,'data.db')))
            
        if os.path.isfile(self['DEBUG_LOG']):
            os.remove(self['DEBUG_LOG'])
            
        if os.path.exists(self['DATABASE']):
            os.remove(self['DATABASE'])