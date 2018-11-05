from os import path, makedirs
import math
from urllib.request import urlopen
import random

def deg2num(lat_deg, lon_deg, zoom):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
    return (xtile, ytile)

def download_url(zoom, xtile, ytile):
    # Switch between otile1 - otile4
    subdomain = random.randint(1, 4)
    
    url = "http://c.tile.openstreetmap.org/%d/%d/%d.png" % (zoom, xtile, ytile)
    dir_path = "tiles/%d/%d/" % (zoom, xtile)
    download_path = "tiles/%d/%d/%d.png" % (zoom, xtile, ytile)
    
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    
    if(not os.path.isfile(download_path)):
        print("downloading {}".format(url))
        source = urlopen(url)
        content = source.read()
        source.close()
        destination = open(download_path,'wb')
        destination.write(content)
        destination.close()
    else: print("skipped {}".format(url))


def get(lat, lon, minzoom=1, maxzoom=15):

    # from 0 to 6 download all
    for zoom in range(minzoom,7,1):
        for x in range(0,2**zoom,1):
            for y in range(0,2**zoom,1):
                download_url(zoom, x, y)

    # from 6 to 15 ranges
    for zoom in range(max(minzoom, 7), int(maxzoom)+1, 1):
        xtile, ytile = deg2num(float(lat)-0.1, float(lon)-0.05, zoom)
        final_xtile, final_ytile = deg2num(float(lat)+0.1, float(lon)+0.05, zoom)

        print("{}:{}-{}/{}-{}".format(zoom, xtile, final_xtile, ytile, final_ytile))
        for x in range(xtile, final_xtile + 1, 1):
            for y in range(ytile, final_ytile - 1, -1):                
                result = download_url(zoom, x, y)
    
get(45.273209, -79.416843, 14, 15)    