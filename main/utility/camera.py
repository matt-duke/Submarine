import io
from time import sleep
import os
try:
    import picamera
finally:
    pass
from utility.base_camera import BaseCamera

import src.config as config 
import logging
logger = logging.getLogger(__name__)


class Camera(BaseCamera):

    @staticmethod
    def frames():                
        with picamera.PiCamera() as camera:
            camera.framerate = config.cam_settings['framerate']
            camera.resolution = config.cam_settings['resolution']
            # let camera warm up
            sleep(2)

            stream = io.BytesIO()
            for _ in camera.capture_continuous(stream, 'jpeg', use_video_port=True):
                # return current frame
                stream.seek(0)
                bimg = stream.read()
                yield bimg
                #sleep(1/config.cam_settings['framerate'])
                # reset stream for next frame
                stream.seek(0)
                stream.truncate()
                    