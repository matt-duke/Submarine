import common

from time import sleep
__name__ = 'HardwareController'

class HardwareController(common.BaseClass):
    def __init__(self):
        common.BaseClass.__init__(self, __name__)
        
    def monitor(self):
        def run():
            print('hello')

        self.addThread('hwctrl_monitor',run,sleep=2).start()