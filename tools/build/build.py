#!/usr/bin/python3

import compileall
from pathlib import Path
import os
import stat
from os.path import join
import subprocess as sp
import json
import shutil
import zlib
import tarfile

HOME = os.getenv("HOME")
ROOT = join(HOME,"Submarine-v2")
TOOLS = join(ROOT, 'tools')
VERSION = join(ROOT, 'configuration', 'version.json')

def crc(file_name):
    if not type(file_name) == list:
        file_name = [file_name]
    ret_val = 0
    prev = 0
    for f in file_name:
        for eachLine in open(f,"rb"):
            prev = zlib.crc32(eachLine, prev)
        ret_val += int("%X"%(prev & 0xFFFFFFFF),16)
    return str(hex(ret_val)).upper()[2:]

def rchmod(path, mask):
    for p in Path(path).glob("**/*.py"):
        os.chmod(str(p), mask)
        
def clear_folder(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.mkdir(path)

def tar_folder(in_path, out_path):
    tf = tarfile.TarFile(out_path, mode='w')
    tf.add(in_path, arcname=('/'))
    print('Writing tar to {}'.format(out_path))
    tf.close()
  
def compile():
    working_dir = join(TOOLS, "build")
    clear_folder(working_dir)
    
    firmware = join(ROOT,'firmware')
    
    compileall.compile_dir(join(ROOT,'main'))
    rchmod(join(ROOT,'main'), 0o500)
    tar_folder(join(ROOT,'main'), join(working_dir,"main.tar"))
    
    sp.check_output('make', cwd=join(firmware,'idle'))
    sp.check_output('make', cwd=join(firmware,'runtime'))
    
    tar_folder(join(ROOT,'firmware','idle'), join(working_dir,"idle.tar"))
    tar_folder(join(ROOT,'firmware','runtime'), join(working_dir,"runtime.tar"))
    
    IdleCrc = crc([join(firmware,"idle",'idle.ino'),join(firmware,"idle",'Makefile')])
    print(IdleCrc)
    exit()
    with open(VERSION, "r+") as f:  
        data = json.load(f)
        data['SBC']["crc"] = crc(join(working_dir,"main.tar"))
        data['MPC']['idle']["crc"] = IdleCrc
        data['MPC']['runtime']["crc"] = crc(join(working_dir,"runtime.tar"))
        f.seek(0)
        json.dump(data, f, indent=2)
        f.truncate()

if __name__ == '__main__':
	compile()
