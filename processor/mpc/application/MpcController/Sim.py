import common
from queue import Queue

class SrcClass(common.BaseClass):
    def __init__(self):
        common.BaseClass.__init__(self)
        
        self.tx_queue = Queue()
        self.rx_queue = Queue()
        
        self.thread_name = 'sim_writer'
        
    def tx(self):
        pass
        
    def rx(self):
        pass
    
    def test(self):
        return True
    
    def start(self):
        def run():
            common.CDS.get('batt_voltage').write(10)
            common.CDS.get('external_press').write(10)
            common.CDS.get('m1_current').write(10)
            common.CDS.get('m2_current').write(10)

        self.addThread(self.thread_name,run,sleep=0.5).start()
        
    def is_running(self):
        if self.thread_name in self.threads.keys():
            return self.threads[self.thread_name].isAlive()
        else:
            return False