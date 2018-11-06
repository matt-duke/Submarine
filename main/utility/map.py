import os
import math
from urllib.request import urlopen
from random import randint
from threading import Thread
from queue import Queue

def deg2num(lat_deg, lon_deg, zoom):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
    return (xtile, ytile)

def thread_worker(q):
    while q != None:
        q.get()()
        q.task_done()
    
def download_url(zoom, xtile, ytile):
    # Switch between otile1 - otile4
    subdomain = randint(1, 4)
    
    url = "http://c.tile.openstreetmap.org/%d/%d/%d.png" % (zoom, xtile, ytile)
    dir_path = "%s/webpage/tiles/%d/%d/" % (os.getcwd(), zoom, xtile)
    download_path = "%s/webpage/tiles/%d/%d/%d.png" % (os.getcwd(), zoom, xtile, ytile)
    
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    
    if(not os.path.isfile(download_path)):
        print("downloading {} -> {}".format(url, download_path))
        source = urlopen(url)
        content = source.read()
        source.close()
        destination = open(download_path,'wb')
        destination.write(content)
        destination.close()
    else: print("skipped {}".format(url))


def get(lat, lon, maxzoom=15):
    q = Queue()
    for i in range(5):
        t = Thread(target = thread_worker, args=(q,))
        t.daemon = True
        t.start()
    # from 0 to 6 download all
    for zoom in range(1,7,1):
        for x in range(0,2**zoom,1):
            for y in range(0,2**zoom,1):
                q.put(download_url(zoom, x, y))

    # from 6 to 15 ranges
    for zoom in range(7, int(maxzoom)+1, 1):
        xtile, ytile = deg2num(float(lat)-0.1, float(lon)-0.05, zoom)
        final_xtile, final_ytile = deg2num(float(lat)+0.1, float(lon)+0.05, zoom)

        print("{}:{}-{}/{}-{}".format(zoom, xtile, final_xtile, ytile, final_ytile))
        for x in range(xtile, final_xtile + 1, 1):
            for y in range(ytile, final_ytile - 1, -1):                
                q.put(download_url(zoom, x, y))
    q = None
  