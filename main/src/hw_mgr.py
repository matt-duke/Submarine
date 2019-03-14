import os
import psutil
from pathlib import Path
from time import sleep
import shutil
import random

import common

class SrcClass(common.data_types.Bus):
    def __init__(self, bus):
        self.bus = bus
        self.logger = bus.logger
        self.bus.add_sensor('total_ram', type=int, check_valid=False)
        self.bus.add_sensor('total_disk', type=int, check_valid=False)
        self.bus.add_sensor('free_ram', type=int)
        self.bus.add_sensor('used_disk', type=int)
        self.bus.add_sensor('ps_ram', type=int)
        self.bus.add_sensor('media_disk', type=int, check_valid=False)
        self.bus.add_sensor('tile_disk', type=int, check_valid=False)
        self.bus.add_sensor('cpu_use', type=int)
        self.bus.add_sensor('cpu_temp', type=float)
        self.bus.add_sensor('fan_speed', type=int, check_valid=False)
        
    def setup(self):
        self.update()
        self.media_path = common.config.get('PATHS','MediaPath')
        self.tile_path = common.config.get('PATHS','TileSavePath')
        self.bus.write('total_ram', self.memory.total)
        self.bus.write('total_disk', self.disk.total)
        self.bus.write('fan_speed', 0)
        self.manual_update()
    
    def manual_update(self):
        self.bus.write('media_disk', self.get_folder_size(self.media_path))
        self.bus.write('tile_disk', self.get_folder_size(self.tile_path))
    
    def loop(self):
        self.update()
        self.bus.write('free_ram', self.memory.available)
        self.bus.write('ps_ram', self.process.memory_info().rss)
        self.bus.write('used_disk', self.disk.used)
        self.bus.write('cpu_use', self.cpu)
        self.bus.write('cpu_temp', self.cpu_temp)
    
    def test(self):
        pass
    
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
        if self.bus.platform == 'Linux':
            self.cpu_temp = psutil.sensors_temperatures()
        else:
            self.cpu_temp = random.randrange(20,75)
        self.process = psutil.Process(os.getpid())
