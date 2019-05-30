from transitions import Machine, State

import common
import core


class OpModeMachine(core.BaseClass):
    states = [State(name='setup'),
              State(name='post'),
              State(name='test'),
              State(name='normal'),
              State(name='upgrade'),
              State(name='critical')]
    
    calibrated = False
    post = False
    
    def __init__(self):
        core.BaseClass.__init__(self)
    
        self.machine = Machine(self, states=OpModeMachine.states, queued=True)
        
        self.machine.add_transition('toCritical', source='*', dest='critical')
        
        self.machine.add_transition('next', source='initial', dest='setup', conditions=['setup_test'])
        self.machine.add_transition('next', source='setup', dest='post')
        self.machine.add_transition('next', source='post', dest='test')
        self.machine.add_transition('next', source='test', dest='normal', conditions=['boot_complete'])
    
        import MpcController
        core.BaseClass.MpcController = MpcController.main()
        import NetController
        core.BaseClass.NetController = NetController.main()
        import HardwareController
        core.BaseClass.HardwareController = HardwareController.main()
        import MotionController
        core.BaseClass.MotionController = MotionController.main()
    
    def boot_complete(self): return self.post and self.calibrated
    
    def setup_test(self): return core.BaseClass.MpcController.POST.start(minimal=True)
    
    def on_enter_setup(self):
        core.BaseClass.MpcController.setup()
        core.BaseClass.HardwareController.Mcu.open_serial()
    
    def on_enter_post(self):
        self.post = core.BaseClass.MpcController.POST.start(minimal=True)
        if self.post:
            self.logger.info('POST finished successfully')
        else:
            self.logger.critical('POST failed.')
            self.toCritical()
    
    def on_enter_test(self):
        pass
    
    def on_enter_upgrade(self):
        self.HardwareController.update_mcu('')
    
    def on_enter_normal(self):
        core.BaseClass.HardwareController.monitor()
        common.CDS.start_logging()
    
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
        