from transitions import Machine, State
from threading import Event
import time

import common
import core


class OpModeMachine(core.BaseClass):
    states = [State(name='setup'),
              State(name='post'),
              State(name='test'),
              State(name='normal'),
              State(name='upgrade'),
              State(name='critical')]
    
    calibrated = True
    post = False
    ready = Event()
    
    def __init__(self):
        core.BaseClass.__init__(self)
    
        self.machine = Machine(self, states=OpModeMachine.states, queued=True, 
                               before_state_change=self.before_state_change,
                               after_state_change=self.after_state_change)
        
        self.machine.add_transition('to_critical', source='*', dest='critical')
        self.machine.add_transition('to_upgrade', source='normal', dest='upgrade')
        
        self.machine.add_transition('next', source='initial', dest='setup', conditions=['setup_test'])
        self.machine.add_transition('next', source='setup', dest='post')
        self.machine.add_transition('next', source='post', dest='test')
        self.machine.add_transition('next', source='test', dest='normal', conditions=['boot_complete'])
    
        import MpcController
        common.MpcController = MpcController.main()
        import NetController
        common.NetController = NetController.main()
        import HardwareController
        common.HardwareController = HardwareController.main()
        import MotionController
        common.MotionController = MotionController.main()
    
    def before_state_change(self):
        self.ready.clear()
        
    def after_state_change(self):
        self.ready.set()
        common.CVT.opmode = self.state
    
    def boot_complete(self):
        resp = self.post and self.calibrated
        if not resp:
            self.ready.clear()
        return resp
    
    def setup_test(self): return common.MpcController.POST.start(minimal=True)
    
    def on_enter_setup(self):
        common.MpcController.setup()
        common.HardwareController.Mcu.connect()
        common.NetController.start()
    
    def on_enter_post(self):
        self.post = common.MpcController.POST.start(minimal=True)
        self.post &= common.HardwareController.mcu_test()
        if self.post:
            self.logger.info('POST finished successfully')
        else:
            self.logger.critical('POST failed.')
            self.to_critical()
    
    def on_enter_test(self):
        time.sleep(100)
    
    def on_exit_test(self):
        pass
        #self.machine.to_upgrade()
    
    def on_enter_upgrade(self):
        self.MpcController.os_update()
        #self.HardwareController.update_mcu('')
    
    def on_enter_normal(self):
        common.HardwareController.monitor()
        #common.CDS.start_logging()
    
    def on_enter_critical(self):
        self.logger.critical('Entering '+self.state)
        common.Active.disable()

        
class ActiveMachine(object):
    states = [State(name='init'),
              State(name='active'),
              State(name='disabled')]
              
    def __init__(self):
        self.machine = Machine(self, states=ActiveMachine.states, initial='active')
        self.machine.add_transition('disable', source='*', dest='disabled')
        