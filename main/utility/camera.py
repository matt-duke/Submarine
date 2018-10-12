import logging
import os

sim = False
try:
    from picamera import PiCamera
except:
    sim = True

class Camera():
    def __init__(self, save_path, res=(1280x720)):
        self.save_path = save_path
        self.res = res
        self.output = "__init__"
        self.cam = None
        if not os.path.isdir(self.save_path):
            os.mkdir(self.save_path)
    
    def start_cam(self):
        if self.cam not None:
            return False
        self.cam = PiCamera()
        self.cam.resolution = self.res
        return True
        
    def close_cam(self):
        if self.cam is None:
            return
        self.cam.close()
        self.cam = None
                
    def take_photo(self):
        filename = "{}/image_{counter}.jpg".format(path)
        logger.debug("take_photo(): {}".format(filename))
        if sim:
            return
        if self.start_cam():
            self.cam.capture(filename)
            logger.debug("take_photo(): Success")
            self.close_cam()
            
    def start_recording(self):
        self.output = self.save_path+'video_{counter}.mp4'
        logger.debug("start_recording(): started {}".format(output))
        if sim:
            return
        if self.start_cam():
            self.cam.start_recording(output, 'h264')
    
    def stop_recording(self):
        logger.debug("stop_recording(): {}".format(self.output))
        if sim:
            return
        if self.cam not None:
            cam.stop_recording()
            self.close_cam()