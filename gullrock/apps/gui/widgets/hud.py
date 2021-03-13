from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import redis
from time import sleep
from threading import Thread

class HUD(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.db = redis.Redis(host='localhost', port=6379, db=0, health_check_interval=10)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.transparency = 100
        self.poll_rate = 1000 #ms
        self.update_thread = Thread()

        self.initUI()
        self.initDatabase()

    def initUI(self):
        self.time = QLabel("##")
        self.depth = QLabel("##")
        self.battery_voltage = QLabel("##")
        self.water_temp = QLabel("##")
        self.pressure = QLabel("123 kPa")
        self.pitch = QLabel("10 deg")
        self.battery_percent = QLabel("79% BAT")
        self.gps = QLabel("4 SAT")
        self.status = QLabel("Active")
        self.conn_speed = QLabel("101 kbps")
        self.cpu = QLabel("55% CPU")

        info_layout = QGridLayout()
        self.info_widget = QWidget()
        self.info_widget.setLayout(info_layout)
        info_layout.addWidget(self.battery_percent, 0, 0)
        info_layout.addWidget(self.conn_speed, 1, 0)
        info_layout.setAlignment(self.battery_percent, Qt.AlignLeft)
        info_layout.setAlignment(self.conn_speed, Qt.AlignLeft)
        info_layout.addWidget(self.gps, 0, 1)
        info_layout.addWidget(self.cpu, 1, 1)
        info_layout.setAlignment(self.gps, Qt.AlignRight)
        info_layout.setAlignment(self.cpu, Qt.AlignRight)


        top_layout = QGridLayout()
        top_layout.addWidget(self.status, 0, 0)
        top_layout.addWidget(self.time, 0, 1)
        top_layout.addWidget(self.info_widget, 0, 2)
        top_layout.setAlignment(self.info_widget, Qt.AlignRight)
        self.top_widget = QWidget()
        self.top_widget.setLayout(top_layout)
        top_layout.setAlignment(self.time, Qt.AlignHCenter | Qt.AlignVCenter)
        top_layout.setAlignment(self.status, Qt.AlignLeft | Qt.AlignVCenter)
        top_layout.setAlignment(self.info_widget, Qt.AlignRight | Qt.AlignTop)
        self.layout.addWidget(self.top_widget)
        self.layout.setAlignment(self.top_widget, Qt.AlignTop)

        bottom_layout = QGridLayout()
        bottom_layout.addWidget(QLabel("Depth"), 0, 0)
        bottom_layout.addWidget(self.depth, 1, 0)
        bottom_layout.addWidget(QLabel("Battery"), 0, 1)
        bottom_layout.addWidget(self.battery_voltage, 1, 1)
        bottom_layout.addWidget(QLabel("Water temp."), 0, 2)
        bottom_layout.addWidget(self.water_temp, 1, 2)
        bottom_layout.addWidget(QLabel("Pressure"), 0, 3)
        bottom_layout.addWidget(self.pressure, 1, 3)
        bottom_layout.addWidget(QLabel("Pitch"), 0, 4)
        bottom_layout.addWidget(self.pitch, 1, 4)
        bottom_layout.setAlignment(Qt.AlignBottom)
        self.bottom_widget = QWidget()
        self.bottom_widget.setLayout(bottom_layout)
        self.layout.addWidget(self.bottom_widget)
        self.layout.setAlignment(self.bottom_widget, Qt.AlignBottom)

    def initDatabase(self):
        def run(self):
            while True:
                try:
                    self.db.ping()
                    self.update_fn()
                except:
                    print("Refresh failed")
                finally:
                    sleep(self.poll_rate/1000)

        if self.update_thread.is_alive():
            print("unable to start poll thread: already active")

        self.update_thread = Thread(target=run, args=(self,))
        self.update_thread.daemon = True
        self.update_thread.start()

    def updateData(self):
        self.depth.setText(f'{float(db.get("depth"))} m')
        self.battery_voltage.setText(f'{float(db.get("battery_voltage"))} V')

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self.top_widget.setFixedWidth(self.width())
        self.top_widget.setFixedHeight(self.bannerHeight())
        self.bottom_widget.setFixedWidth(self.width())
        self.bottom_widget.setFixedHeight(self.bannerHeight())
        self.info_widget.setFixedWidth(self.width()*0.2)
        self.info_widget.setFixedHeight(self.bannerHeight())

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawHeader(qp)
        self.drawFooter(qp)
        qp.end()

    def bannerHeight(self):
        return self.height()*0.12

    def drawHeader(self, qp):
        grey = QColor(10, 10, 10, self.transparency)
        white = QColor(255, 255, 255, self.transparency)
        qp.setBrush(grey)
        qp.setPen(white)

        qp.drawRect(0, 0, self.width(), self.bannerHeight())

    def drawFooter(self, qp):
        grey = QColor(10, 10, 10, self.transparency)
        white = QColor(255, 255, 255, self.transparency)
        qp.setBrush(grey)
        qp.setPen(white)

        num_div = 5
        space = self.width() / num_div
        for i in range(num_div):
            x1 = i*space
            qp.drawRect(x1, self.height()-self.bannerHeight(), space, self.height())
