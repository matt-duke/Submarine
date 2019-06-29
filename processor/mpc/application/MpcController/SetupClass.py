import core
import common

import os

class SetupClass(core.BaseClass):
    def __init__(self):
        core.BaseClass.__init__(self)
        
        self.default = common.defaults.load()
        if not self.is_valid():
            self.logger.critical('Default file is not valid')
    
    def run(self):
        self.__networking()
        self.__paths()
        
        self.__cleanup()
    
    def __networking(self):
        for key, ntwrk in self.default['network'].items():
            if 'vlan' in ntwrk:
                self.systemCall('vconfig add eth0 {}'.format(ntwrk['vlan']))
            self.systemCall('ifconfig eth0.{} {}'.format(ntwrk['vlan'], ntwrk['mpc_ip']))
            
    def __paths(self):
        for key, path in self.default['paths'].items():
            p = os.path.join(self.default[path['basename']], path['filename'])
            common.Paths.add(key, p)
            
    def __cleanup(self):
        for key, path in common.Paths.items():
            if not os.path.exists(path):
                self.logger.info('Generating empty file for {}'.format(path))
                open(path, 'w').close()