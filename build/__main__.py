#!/usr/bin/python3

import configparser
from pathlib import Path
import os
import stat
from os.path import join, dirname
import subprocess as sp
import json
import shutil
import zlib
import tarfile

def getEnv(key, default):
    env = os.environ.get(key, default)
    if env == default:
        return env
    elif env.lower() in ('false', 'no'):
        env=False
    elif env.lower() in ('true', 'yes'):
        env=True
    return env

OPTIMIZE=getEnv('OPTIMIZE', False)
if OPTIMIZE:
    os.environ['PYTHONOPTIMIZE'] = '1'
BUILD_FIRMWARE=getEnv('BUILD_FIRMWARE', False)
BUILD_IMAGES=getEnv('BUILD_IMAGES', False)
COMPILE=getEnv('COMPILE',True)

ROOT = getEnv('ROOT',dirname(dirname(os.path.realpath(__file__))))
print(ROOT)
SW_DIR = join(ROOT, 'processor')
FIRMWARE_DIR = join(ROOT, 'firmware')
FIRMWARE_DIRS = ['idle', 'runtime']
CONFIG = join(ROOT, 'configuration')
VERSION = join(ROOT, 'configuration', 'version.json')
WORK=join(ROOT, 'work')
DEPLOY=join(ROOT,'deploy')

def copytree(src, dst, symlinks=False, ignore=None):
    ignore = shutil.ignore_patterns(*ignore)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            if len(ignore(path=src, names=[item])) == 0:
                shutil.copy2(s, d)

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
        for obj in os.listdir(path):
            obj=join(path,obj)
            print('Removing '+obj)
            if os.path.isdir(obj):
                shutil.rmtree(obj)
            else:
                os.remove(obj)

def tar_folder(in_path, out_path):
    tf = tarfile.TarFile(out_path, mode='w')
    tf.add(in_path, arcname=('/'))
    print('Writing tar to {}'.format(out_path))
    tf.close()

def build():
    print('Building firmware')
    for file in FIRMWARE_DIRS:
        print('Building {}...'.format(file))
        sp.check_output('make', cwd=join(FIRMWARE_DIR, file))
        tar_folder(join(ROOT,'firmware',file), join(WORK, file+'.tar'))
        print('...Done')

def compile():
    work_dir = join(WORK, 'application')
    MAKEFILE = join(SW_DIR, 'Makefile.ini')
    IGNORE = ['README.txt']
    cfg = configparser.ConfigParser()
    cfg.read(MAKEFILE)
    folders = list()
    for s in cfg.sections():
        if s == 'DEFAULT':
            continue
        p = cfg.getint(s, 'Priority', fallback=None)
        if p == None:
            folders.append(s)
        else:
            folders.insert(p, s)
    #build working directory
    for folder in folders:
        dstList = cfg.get(folder, 'CopyContentsTo', fallback=folder).replace(' ', '').split(',')
        for dst in dstList:
            src = join(SW_DIR,folder)
            dst = join(work_dir, dst)
            ignore = cfg.get(folder, 'Ignore').replace(' ', '').split(',')
            copytree(src, dst, ignore=ignore)

    if OPTIMIZE:
        import PyInstaller.__main__
        for app in os.listdir(work_dir):
            print('Compiling {}'.format(app))
            PyInstaller.__main__.run([
                '--name={}'.format(app),
                '--onedir',
                '--exclude-module={}'.format('pyinstaller'),
                '--distpath={}'.format(join(DEPLOY,'application')),
                '--noconfirm',
                '--workpath={}'.format(join(WORK, 'pyinstaller')),
                join(work_dir, app, 'application', 'bootsequence.py'),
            ])
        #tar_folder(work_dir, join(DEPLOY,dir+'.tar'))

def write_sw_config():
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

def run():
    BUILD_FIRMWARE=False
    COMPILE=True
    CLEAN=True
    print('Starting...')
    if CLEAN:
        clear_folder(WORK)
    if BUILD_FIRMWARE:
        build()
    else:
        print('Skipping firmware building stage')
    if COMPILE:
        compile()
    else:
        print("Skipping compile stage")

    print("Done.")

if __name__ == '__main__':
    run()
