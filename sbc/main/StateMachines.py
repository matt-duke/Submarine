from transitions import Machine, State
import logging
logger=logging.getLogger(__name__)

import common


class OpModeMachine(object):
    states = [State(name='setup'),
              State(name='test'),
              State(name='normal'),
              State(name='upgrade'),
              State(name='critical')]
    
    calibrated = False
    post = False
    
    def __init__(self):
        self.machine = Machine(self, states=OpModeMachine.states)
        
        self.machine.add_transition('toNormal', source='*', dest='normal', conditions=['boot_complete'])
        self.machine.add_transition('toSetup', source='*', dest='setup')
        self.machine.add_transition('toTest', source='*', dest='test')

    def boot_complete(self):
        return self.post and self.calibrated
    
    def on_enter_setup(self):
        logger.info('Entering '+self.state)
        common.config = common.Setup.import_configuration()
        common.Setup.start_logging()
        common.InterfaceManager.importSrc()
        
    def on_enter_test(self):
        logger.info('Entering '+self.state)
        self.post = common.InterfaceManager.testAll()
        #common.POST.start()
    
    def on_enter_normal(self):
        logger.info('Entering '+self.state)
        common.InterfaceManager.startAll()
        common.HardwareController.monitor()
        common.CDS.start_logging()
    
    def on_enter_critical(self):
        common.HardwareController.closeAllThreads(True)
        
class ActiveMachine(object):
    states = [State(name='init'),
              State(name='active'),
              State(name='disabled')]
              
    def __init__(self):
        self.machine = Machine(self, states=OpModeMachine.states)
        