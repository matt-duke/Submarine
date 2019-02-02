import os
import psutil
from pathlib import Path
from time import sleep
import shutil

import common

class SrcClass():
    def __init__(self, bus):
        self.bus = bus
        self.logger = bus.logger
        
        self.bus.add_sensor('total_ram', type=int, check_valid=False)
        self.bus.add_sensor('total_disk', type=int, check_valid=False)
        self.bus.add_sensor('free_ram', type=int)
        self.bus.add_sensor('used_disk', type=int)
        self.bus.add_sensor('ps_ram', type=int)
        self.bus.add_sensor('media_disk', type=int)
        self.bus.add_sensor('tile_disk', type=int)
        self.bus.add_sensor('cpu_use', type=int)
        
    def setup(self):
        self.update()
        self.media_path = common.config['PATHS']['MediaPath']
        self.tile_path = common.config['PATHS']['TileSavePath']
        self.bus.write('total_ram', self.memory.total)
        self.bus.write('total_disk', self.disk.total)
    
    def loop(self):
        self.update()
        self.bus.write('free_ram', self.memory.available)
        self.bus.write('ps_ram', self.process.memory_info().rss)
        self.bus.write('media_disk', self.get_folder_size(self.media_path))
        self.bus.write('tile_disk', self.get_folder_size(self.tile_path))
        self.bus.write('used_disk', self.disk.used)
        self.bus.write('cpu_use', self.cpu)
    
    def test(self):
        pass
    
    def get_folder_size(self, path):
        size = 0
        path = Path(path)
            
        for curr_path, dirs, files in os.walk(path):
            for f in files:
                fp = os.path.join(curr_path, f)
                size += os.path.getsize(fp)
        return size
    
    def update(self):
        self.memory = psutil.virtual_memory()
        self.disk = shutil.disk_usage(Path('/'))
        self.cpu = psutil.cpu_percent(interval=None, percpu=False)
        self.process = psutil.Process(os.getpid())
