import common
from threading import Thread
import os
import psutil
from pathlib import Path
from time import sleep
import shutil

class SrcClass():
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
    
    def run(self):
        self.bus.logger.debug('Starting thread')
        self.update()
        media_path = common.config['PATHS']['MediaPath']
        tile_path = common.config['PATHS']['TileSavePath']
        self.bus['total_ram'].write(self.memory.total)
        self.bus['total_disk'].write(self.disk.total)
        while True:
            self.update()
            self.bus['free_ram'].write(self.memory.available)
            self.bus['ps_ram'].write(self.process.memory_info().rss)
            self.bus['media_disk'].write(self.get_folder_size(media_path))
            self.bus['tile_disk'].write(self.get_folder_size(tile_path))
            self.bus['used_disk'].write(self.disk.used)
            self.bus['cpu_use'].write(self.cpu)
            sleep(self.delay)
