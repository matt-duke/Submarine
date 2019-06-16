#!/bin/bash

cd $WORKSPACE

sw_config=$WORKSPACE/processor/configuration/expected_sw_config.json

mkdir $WORKSPACE/working
mkdir working/image
mkdir working/firmware

venv=$WORKSPACE/working/image/venv

python3 -m pip install virtualenv 
python3 -m virtualenv $venv
$venv/bin/pip install -r ./tools/build/requirements.txt

#make -C ./firmware/runtime/runtime.ino
make -C ./firmware/update
cp ./firmware/update/build-mega2560/update.hex ./working/firmware/update.hex

cp -r ./processor/mpc/application/* ./working/image/
cp -r ./processor/common/* ./working/image/

cp ./processor/mpc/scripts/uboot ./working/uboot

tar -cf ./working/image.tar ./working/image
cd ./working/image && tar -zcf ../image.tar . && cd - 
cp image.tar ./working/image.tar

image_crc=`cksum ./working/image.tar | grep -o '^[[:digit:]]*'`
uboot_crc=`cksum ./working/uboot | grep -o '^[[:digit:]]*'`
mcu_update_crc=`cksum ./working/firmware/update.hex | grep -o '^[[:digit:]]*'`

pat=".MCU.update.crc=$mcu_update_crc | \
.MPC.image.crc=$image_crc | \
.MPC.uboot.crc=$uboot_crc"

jq -n 'env.pat' $sw_config > working/expected_sw_config.json

cd ./working/ && tar -zcf ../build_$BUILD_NUMBER.tgz . && cd - 
