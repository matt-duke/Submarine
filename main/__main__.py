print('ROV Submarine')
print('v.0.1\n')

from statemachine import StateMachine, State
import logging
logger = logging.getLogger(__name__)

class OpModeStateMachine(StateMachine):
    setup = State('Startup', initial=True)
    test = State('Test')
    normal = State('Normal')
    critical = State('Critical')
    
    def __init__(self):
        StateMachine.__init__(self)
    
    def on_enter_startup(self):
        logger.debug('Transition to OpMode:startup')
        
    def on_enter_test(self):
        logger.debug('Transition to OpMode:test')
    
    def on_enter_normal(self):
        logger.debug('Transition to OpMode:normal')
        
    def on_enter_critical(self):
        logger.critical('Transition to OpMode:critical')
        
common.OpMode = OpModeStateMachine()