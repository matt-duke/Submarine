import os
import psutil
from pathlib import Path
from time import sleep
import shutil
import random

import common
from common.data_types import Bus

class SrcClass(Bus):
    def __init__(self):
        Bus.__init__(self, "HwMgr")
        self.add_sensor('total_ram', type=int, check_valid=False)
        self.add_sensor('total_disk', type=int, check_valid=False)
        self.add_sensor('free_ram', type=int)
        self.add_sensor('used_disk', type=int)
        self.add_sensor('ps_ram', type=int)
        self.add_sensor('media_disk', type=int, check_valid=False)
        self.add_sensor('tile_disk', type=int, check_valid=False)
        self.add_sensor('cpu_use', type=int)
        self.add_sensor('cpu_temp', type=float)
        self.add_sensor('fan_speed', type=int, check_valid=False)
        
    def setup(self):
        self.update()
        self.media_path = common.config.get('PATHS','MediaPath')
        self.tile_path = common.config.get('PATHS','TileSavePath')
        self.write('total_ram', self.memory.total)
        self.write('total_disk', self.disk.total)
        self.write('fan_speed', 0)
        self.manual_update()
    
    def manual_update(self):
        self.write('media_disk', self.get_folder_size(self.media_path))
        self.write('tile_disk', self.get_folder_size(self.tile_path))
    
    def loop(self):
        self.update()
        self.write('free_ram', self.memory.available)
        self.write('ps_ram', self.process.memory_info().rss)
        self.write('used_disk', self.disk.used)
        self.write('cpu_use', self.cpu)
        self.write('cpu_temp', self.cpu_temp)
    
    def connection_test(self):
        return True
    
    def get_folder_size(self, path):
        size = 0
        path = Path(path)
        
        for path, dirs, files in os.walk(path):
            for f in files:
                size +=  os.path.getsize(os.path.join(path, f))
                #print('slow')
        return size
    
    def update(self):
        self.memory = psutil.virtual_memory()
        self.disk = shutil.disk_usage(Path('/'))
        self.cpu = psutil.cpu_percent(interval=None, percpu=False)
        if self.platform == 'Linux':
            self.cpu_temp = psutil.sensors_temperatures()
        else:
            self.cpu_temp = random.randrange(20,75)
        self.process = psutil.Process(os.getpid())
