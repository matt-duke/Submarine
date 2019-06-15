#!/bin/bash

cd $WORKSPACE

mkdir image

python3 -m pip install virtualenv 
python3 -m virtualenv venv
./venv/bin/pip install -r ./tools/build/requirements.txt

#make -C ./firmware/runtime/runtime.ino
make -C firmware/update/update.ino
cp firmware/update/build-mega2560/update.hex image/update.hex

tar -czf image_$BUILD_NUMBER.tar.gz image/*