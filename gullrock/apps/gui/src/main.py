import sys

from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from widgets.hud import HUD
from widgets.video import VideoStream
from gamepad import Gamepad
from worker import Worker

# Restore PyQt5 debug behaviour (print exception) https://stackoverflow.com/questions/33736819/pyqt-no-error-msg-traceback-on-exit
def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)

sys.excepthook = except_hook

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.stream = VideoStream()
        self.winId = self.stream.winId()
        self.setCentralWidget(self.stream)

        self.resize(500, 500)

        self.gamepad = Gamepad()

        self.hud = HUD(self)

        #flags = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint)# | QtCore.Qt.WindowStaysOnTopHint)
        #self.setWindowFlags(flags)

    def start(self):
        #self.stream.start()
        self.gamepad.start()

    def resizeEvent(self, e):
        self.hud.resize(self.size())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window.start()
    sys.exit(app.exec_())
