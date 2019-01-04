import piexif
import re
import os
from datetime import datetime
        
        
# exif_dict=piexif.load('maxresdefault.jpg')
# exif_dict['GPS'] = {piexif.GPSIFD.GPSVersionID: (2, 0, 0, 0),
           # piexif.GPSIFD.GPSAltitudeRef: 1,
           # piexif.GPSIFD.GPSDateStamp: u"1999:99:99 99:99:99",
           # }

# exif_bytes = piexif.dump(exif_dict)
# piexif.insert(exif_bytes, 'maxresdefault.jpg')
# exif_dict = piexif.load("maxresdefault.jpg")
# print(exif_dict)


class Gallery:
    class Img:
        def __init__(self, path):
            self.path = path
            self.gps = (0,0,0)
            self.date = (0,0,0)
            self.time = (0,0,0,0)
            self.epoch = 0
            self.exif_dict = None
    
    def __init__(self, path=os.getcwd()):
        self.img=[]
        self.path = path
            
    def load(self, path='.'):
        for root, dirs, files in os.walk(path):
            for file in files:
                if any(f in file for f in ['.jpeg', '.jpg']):
                    image = self.Img(r'{}\{}'.format(root,file))
                    image.exif_dict = piexif.load(image.path)
                    self.add(image)
                
    def add(self, image):
        if isinstance(image, str):
            image = self.Img(image)
            dt = datetime.now()
            image.date = dt[0:2]
            image.time = dt[3:5]
            gps_ifd = {
                piexif.GPSIFD.GPSLatitude: (366132304, 10000000),
                piexif.GPSIFD.GPSLongitude: (1219323420, 10000000),
                piexif.GPSIFD.GPSAltitude: (100,1),
                piexif.GPSIFD.GPSDateStamp: u"{:04d}:{:02d}:{:02d} {:02d}:{:02d}:{:02d}".format(*image.date, *image.time) }
            image.exif_dict = {"GPS":gps_ifd}
            piexif.insert(piexif.dump(image.exif_dict), image.path)
        else:
            lat = image.exif_dict["GPS"][piexif.GPSIFD.GPSLatitude]
            lon = image.exif_dict["GPS"][piexif.GPSIFD.GPSLongitude]
            alt = image.exif_dict["GPS"][piexif.GPSIFD.GPSAltitude]
            image.gps = (lat[0]/lat[1], lon[0]/lon[1], alt[0]/alt[1])
            image.date, image.time = image.exif_dict["GPS"][piexif.GPSIFD.GPSDateStamp].decode("UTF-8").split(' ')
            image.date = tuple(int(i) for i in image.date.split(':'))
            image.time = tuple(int(i) for i in image.time.split(':'))
            image.epoch = datetime(*image.date, *image.time).timestamp()
        self.img.append(image)
        self.sort()
    
    def write(self):
        with open(self.path, 'w') as html:
            html.write('line')
    
    def load_html(self):
        html = open(path, 'r').readlines()
        i=0
        div_index=0
        for line in html:
            if 'id="gallery"' not in line and div_index == 0:
                continue
            if '<div' in line:
                div_index += 1
            
            if '<img' in line:
                image = Img()
                line = re.search('(<img.*>)', line).group(1)
                imgage.path = repr(re.search('src=()', line).group(1))
                r = re.search('class="([^\n"]*)"', line)
                class_list = r[1].split(' ')
                for item in class_list:
                    item = item.split('-')
                    image.__dict__[item[0]] = tuple(item[1:len(item)])
                image.epoch = datetime(image.date + image.time).timestamp()
            if '</div>' in line:
                div_index -= 1
            i += 1
        
    def sort(self):
        def key(img):
            return(img.epoch)
        self.img.sort(key=key)

