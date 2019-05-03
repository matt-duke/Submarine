import io
import time as tm
import os
import piexif
import common
try:
    import picamera
except:
    pass
from .base_camera import BaseCamera
    
import logging
logger = logging.getLogger(__name__)


class Camera(BaseCamera):    
    def save_frame(self, frame, add_to_path = ''):
        if self.b_image:
            add_to_path = 'images'
            self.b_image = False
        elif self.b_video:
            add_to_path = 'videos/tmp'
        else:
            return
        count = len(os.listdir(image_save_path))
        file = open(image_save_path+'/img_{:05d}.jpeg'.format(count),'wb') 
        file.write(bytearray(frame))
        file.close()
    
    @staticmethod
    def frames():                
        with picamera.PiCamera() as camera:
            camera.framerate = common.config['camera']['framerate']
            camera.resolution = (common.config['camera']['resolutionwidth'],common.config['camera']['resolutionwidth'])
            # let camera warm up
            time.sleep(2)

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
                    
if __name__ == '__main__':
    time = tm.localtime(tm.time())
    exif_dict = piexif.load("maxresdefault.jpg")
    print(exif_dict['GPS'])
    exif_dict['GPS'] = {
        piexif.GPSIFD.GPSVersionID: (0, 0, 0, 0),
        piexif.GPSIFD.GPSAltitudeRef: 1, #above or below sea level
        piexif.GPSIFD.GPSAltitude: 40,
        piexif.GPSIFD.GPSDateStamp: u"{:04d}:{:02d}:{:02d} {:02d}:{:02d}:{:02d}".format(time.tm_year, time.tm_mon, time.tm_mday, time.tm_hour, time.tm_min, time.tm_sec) }
    #exif_bytes = piexif.dump(exif_dict)
    #piexif.insert("maxresdefault", exif_bytes)
    
    print(exif_dict)