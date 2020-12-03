# !/usr/bin/python3

import json
import zlib
import os

PLATFORM = "mpc"
FILE = 'test.json'

def file_crc32(filename):
    with open(filename, 'rb') as fh:
        hash = 0
        while True:
            s = fh.read(65536)
            if not s:
                break
            hash = zlib.crc32(s, hash)
        return "%08X" % (hash & 0xFFFFFFFF)

def get_crc_dict(path):
    d = dict()
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            file_path = os.path.join(root, name)
            key = file_path.replace(path, "")
            d[key] = {'crc': file_crc32(file_path),
                      'name': name
            }
        for name in dirs:
            pass
            #print(os.path.join(root, name))
    return d

if __name__ == '__main__':
    data = dict()
    base_path = "./config/files"
    folders = [os.path.join(base_path, PLATFORM), os.path.join(base_path, "common")]
    for folder in folders:
        data = {**data, **get_crc_dict(folder)}
    
    with open(FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)