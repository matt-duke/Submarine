import sys
import gi
gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class VideoStream(QWidget):

    def __init__(self):
        super().__init__()

    def connect(self):
        try:
            #test connection
            self.init_pipeline()
        except:
            self.pipeline_failed()

    def pipeline_failed(self):
        self.layout = QVBoxLayout()
        self.painter = QPainter
        self.painter.setPen(Qt.blue)
        self.painter.setFont(QFont("Arial", 30))
        self.painter.drawText("Test", Qt.AlignCenter, "Qt")
        self.layout.addWidget(self.painter)
        self.setLayout(self.layout)

    def init_pipeline(self):
        GObject.threads_init()
        Gst.init(None)

        self.pipeline = Gst.Pipeline()
        self.tcpsrc = Gst.ElementFactory.make('tcpclientsrc', 'tcpsrc')
        self.tcpsrc.set_property('host', '192.168.10.168')
        self.tcpsrc.set_property('port', 5000)
        self.gdepay = Gst.ElementFactory.make('gdpdepay', 'gdepay')
        self.rdepay = Gst.ElementFactory.make('rtph264depay', 'rdepay')
        self.avdec = Gst.ElementFactory.make('avdec_h264', 'avdec')
        self.vidconvert = Gst.ElementFactory.make('videoconvert', 'vidconvert')
        self.asink = Gst.ElementFactory.make('autovideosink', 'asink')
        self.asink.set_property('sync', False)
        self.pipeline.add(self.tcpsrc)
        self.pipeline.add(self.gdepay)
        self.pipeline.add(self.avdec)
        self.pipeline.add(self.rdepay)
        self.pipeline.add(self.vidconvert)
        self.pipeline.add(self.asink)
        self.tcpsrc.link(self.gdepay)
        self.gdepay.link(self.rdepay)
        self.rdepay.link(self.avdec)
        self.avdec.link(self.vidconvert)
        self.vidconvert.link(self.asink)
        bus = self.pipeline.get_bus()
        
        bus.add_signal_watch()
        bus.enable_sync_message_emission()
        bus.connect('message', self.on_message)
        bus.connect('sync-message::element', self.on_sync_message)

    def on_message(self, bus, message):
        t = message.type
        if t == Gst.MESSAGE_EOS:
            self.pipeline.set_state(Gst.State.NULL)
        elif t == Gst.MESSAGE_ERROR:
            err, debug = message.parse_error()
            print('Error: %s' % err, debug)
            self.pipeline.set_state(Gst.State.NULL)

    def on_sync_message(self, bus, message):
        if message.structure is None:
            return
        message_name = message.structure.get_name()
        if message_name == 'prepare-xwindow-id':
            assert self.winId
            imagesink = message.src
            imagesink.set_property('force-aspect-ratio', True)
            imagesink.set_xwindow_id(win_id)

    def startPrev(self):
        self.pipeline.set_state(Gst.State.PLAYING)

    def pausePrev(self):
        self.pipeline.set_state(Gst.State.NULL)