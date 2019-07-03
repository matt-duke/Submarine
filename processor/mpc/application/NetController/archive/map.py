import os
import math
from urllib.request import urlopen
from random import randint
from threading import Thread
from queue import Queue
from os import path, getcwd

class Map:
    def __init__(self, main_self):
        self.tile_save_path = main_self.tile_save_path
        
    def deg2num(self, lat_deg, lon_deg, zoom):
        lat_rad = math.radians(lat_deg)
        n = 2.0 ** zoom
        xtile = int((lon_deg + 180.0) / 360.0 * n)
        ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
        return (xtile, ytile)

    def thread_worker(self, q):
        while q != None:
            task = q.get()
            task[0](task[1])
            q.task_done()
        
    def download_url(self, data):
        zoom, xtile, ytile, tile_folder = str(data[0]), str(data[1]), str(data[2]), data[3]
        # Switch between otile1 - otile4
        #subdomain = randint(1, 4)
        ext = 'jpg'
        url = "https://server.arcgisonline.com/ArcGIS/rest/services/NatGeo_World_Map/MapServer/tile/{}/{}/{}".format(zoom, xtile, ytile)
        dir_path = path.join(getcwd(), tile_folder, zoom, xtile)
        save_path = str(path.join(getcwd(), tile_folder, zoom, xtile, ytile))+'.'+ext
        
        if not os.path.exists(dir_path):
            try:
                os.makedirs(dir_path)
            except FileExistsError:
                print("forlder already exists: "+dir_path)
        
        if(not os.path.isfile(save_path)):
            print("downloading {} -> {}".format(url, save_path))
            source = urlopen(url)
            content = source.read()
            source.close()
            destination = open(save_path,'wb')
            destination.write(content)
            destination.close()
        else: print("skipped {}".format(url))
        
    def clear_tiles(self):
         folders = [f.path for f in os.scandir(self.tile_save_path) if f.is_dir()]
         for f in folders:
            os.rmdir(f)

    def get(self, lat, lon, maxzoom=13):
        q = Queue()
        for i in range(5):
            t = Thread(target = self.thread_worker, args=(q,))
            t.daemon = True
            t.start()
        # from 0 to 6 download all
        for zoom in range(1,7,1):
            for x in range(0,2**zoom,1):
                for y in range(0,2**zoom,1):
                    q.put((self.download_url, (zoom, x, y,  self.tile_save_path)))

        # from 6 to 15 ranges
        for zoom in range(7, int(maxzoom)+1, 1):
            xtile, ytile = self.deg2num(float(lat)-0.1, float(lon)-0.05, zoom)
            final_xtile, final_ytile = self.deg2num(float(lat)+0.1, float(lon)+0.05, zoom)

            print("{}:{}-{}/{}-{}".format(zoom, xtile, final_xtile, ytile, final_ytile))
            for x in range(xtile, final_xtile + 1, 1):
                for y in range(ytile, final_ytile - 1, -1):                
                    q.put((self.download_url, (zoom, x, y,  self.tile_save_path)))
        q = None
  