#!/bin/bash

cd $WORKSPACE
python3 -m pip install virtualenv 
python3 -m virtualenv venv
./venv/bin/pip install -r ./tools/build/requirements.txt

make ./firmware/runtime/runtime.ino
make ./firmware/update/update.ino

tar -czf image_$BUILD_NUMBER.tar.gz *