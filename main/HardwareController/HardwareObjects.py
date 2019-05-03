from transitions import Machine
import logging
logger = logging.getLogger(__name__)

class Light(object):
    def __init__(self):
        self.machine = Machine(self, states=['on', 'off'])
        self.machine.add_transition('toggle', 'on', 'off')
        self.machine.add_transition('toggle', 'off', 'on')
        self.to_off()

    def on_enter_on(self):
        logger.info('Light on')
        
    def on_enter_off(self):
        logger.info('Light off')

class Fan(object):
    def __init__(self):
        self.speed = 0
        self.machine = Machine(self, states=['enabled', 'disabled'])
        self.machine.add_transition('toggle', 'enabled', 'disabled')
        self.machine.add_transition('toggle', 'enabled', 'disabled')
        self.to_enabled()

    def on_enter_enabled(self): logger.info('Fan enabled')
    def on_enter_disabled(self): logger.info('Fan disabled')
    def setSpeed(self, percent):
        if self.state.is_disabled():
            return
        self.speed = percent * 5