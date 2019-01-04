import common
from threading import Thread, enumerate
import os
import psutil
from pathlib import Path
from time import sleep
import shutil


class HwManager(Thread):
    def __init__(self):
        self.delay = 2
        Thread.__init__(self, daemon = False)

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
        self.update()
        media_path = common.config['PATHS']['MediaPath']
        tile_path = common.config['PATHS']['TileSavePath']
        common.sensors['total_ram'].write(self.memory.total)
        common.sensors['total_disk'].write(self.disk.total)
        while True:
            self.update()
            common.sensors['free_ram'].write(self.memory.available)
            common.sensors['ps_ram'].write(self.process.memory_info().rss)
            common.sensors['media_disk'].write(self.get_folder_size(media_path))
            common.sensors['tile_disk'].write(self.get_folder_size(tile_path))
            common.sensors['used_disk'].write(self.disk.used)
            temp = common.sensors['used_disk'].read(do_not_update=True)
            for i in ['tile_disk','media_disk']:
                temp = temp - common.sensors[i].read(do_not_update=True)
            common.sensors['other_disk'].write(temp)
            common.sensors['cpu_percent'].write(self.cpu)
            print(self.cpu)
            sleep(self.delay)
