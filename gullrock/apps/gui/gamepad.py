import inputs
import redis
from threading import Thread
from time import sleep
from definitions import *
from PyQt5.QtCore import QObject, pyqtSignal

POLL_RATE = 10 #Hz


class GamepadSignals(QObject):
    MOTOR_R = pyqtSignal(float)
    MOTOR_L = pyqtSignal(float)
    HEADLIGHT = pyqtSignal(bool)
    DPAD_X = pyqtSignal(int)

class Gamepad(Thread):
    def __init__(self):
        super().__init__()

        self.daemon = True
        self.signals = GamepadSignals()

        try:
            self.db = redis.Redis(host='localhost', port=6379, db=0, health_check_interval=10)
            self.pubsub = self.db.pubsub()
        except:
            print("No redis server")

    def run(self):
        while True:
            try:
                events = inputs.get_gamepad()
                for event in events:
                    #print(event.ev_type, event.code, event.state)
                    if event.code == "ABS_RZ":
                        self.setMotorR(event.state)
                    elif event.code == "ABS_Z":
                        self.setMotorL(event.state)
                    elif event.code == "BTN_TR" and event.state == 0:
                        self.setHeadlight()
                    elif event.code == "ABS_HAT0X":
                        self.dPad(event.state)
                    else:
                        pass#print(event.code, event.state)
            except inputs.UnpluggedError as e:
                print("No gamepad connected.")
                return

    def dPad(self, state):
        self.signals.DPAD_X.emit(state)

    def setMotorL(self, state):
        print(f"Setting L motor: {state}")
        self.signals.MOTOR_L.emit(state)
        self.pubsub.publish(PubSub.MOTOR_L, state)

    def setMotorR(self, state):
        print(f"Setting R motor {state}")
        self.signals.MOTOR_R.emit(state)
        self.pubsub.publish(PubSub.MOTOR_R, state)

    def setHeadlight(self):
        curr_state = self.db.get(RedisChannel.HEADLIGHT_STATE)
        state = not curr_state
        print(f"Setting headlight state {state}")
        self.db.set(RedisChannel.HEADLIGHT_STATE, state)

        self.signals.HEADLIGHT.emit(state)
        self.pubsub.publish(PubSub.HEADLIGHT, state)

if __name__ == '__main__':
    g = Gamepad()
    g.start()
    while True:
        pass
