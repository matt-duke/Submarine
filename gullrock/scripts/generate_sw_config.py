# !/usr/bin/python3

import json
import zlib
import os
from pathlib import Path

platform = "mpc"
file_out = Path(__file__).parent.joinpath('test.json').absolute()
base_path = Path(__file__).parent.joinpath("../apps/config_controller/config/files").absolute()

print(os.listdir(base_path))

def file_crc32(filename):
    with open(filename, 'rb') as fh:
        hash = 0
        while True:
            s = fh.read(65536)
            if not s:
                break
            hash = zlib.crc32(s, hash)
        return int("%08X" % (hash & 0xFFFFFFFF), 16)

def get_crc_dict(dirpath):
    dirpath = os.path.abspath(dirpath)
    file_list = list()
    for root, dirs, files in os.walk(dirpath, topdown=False):
        for name in files:
            file_path = os.path.abspath(os.path.join(root, name))
            path = file_path.replace(dirpath, "")
            file_list.append({'crc': file_crc32(file_path)
                          'name': name,
                          'path': path
            })
        for name in dirs:
            pass
            #print(os.path.join(root, name))
    print(file_list)
    return file_list

def app_version_list():
    app_list = {
        'redis-server': "6.0.9",
        'libgstreamer1.0-dev': '0.0.0',
        'libgstreamer-plugins-base1.0-dev': '0.0.0.0'
    }
    return app_list

if __name__ == '__main__':
    data = dict()
    data['files'] = list()
    folders = [os.path.join(base_path, platform), os.path.join(base_path, "common")]
    for folder in folders:
        crc_list = get_crc_dict(folder)
        #print(folder)
        data['files'] = data['files'] + crc_list
    app_versions = app_version_list()
    data[]
    with open(file_out, 'w', encoding='utf-8') as f:
        print("Dumping to {}".format(file_out))
        json.dump(data, f, ensure_ascii=False, indent=4)