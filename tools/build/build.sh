#!/bin/bash

cd $WORKSPACE

sw_config=$WORKSPACE/processor/configuration/expected_sw_config.json

mkdir $WORKSPACE/image
mkdir $WORKSPACE/firmware

image=$WORKSPACE/image/image.pex

python3 -m pip install pex

#make -C ./firmware/runtime/runtime.ino
make -C ./firmware/update
cp ./firmware/update/build-mega2560/update.hex ./firmware/update.hex

#cp -r ./processor/mpc/application/* ./image/
#cp -r ./processor/common/* ./image/

#https://pex.readthedocs.io/en/stable/buildingpex.html#buildingpex
pex --python=python3.5 -r ./tools/build/requirements.txt -c ./processor/mpc/application/bootsequence.py -o $python

cp ./processor/mpc/scripts/uboot ./uboot

cd ./image && tar -zcf ../image.tar . && cd - 
cp image.tar ./working/image.tar

image_crc=`cksum ./image.tar | grep -o '^[[:digit:]]*'`
uboot_crc=`cksum ./uboot | grep -o '^[[:digit:]]*'`
mcu_update_crc=`cksum ./firmware/update.hex | grep -o '^[[:digit:]]*'`

pat=".MCU.update.crc=$mcu_update_crc | \
.MPC.image.crc=$image_crc | \
.MPC.uboot.crc=$uboot_crc"

jq -n 'env.pat' $sw_config > expected_sw_config.json

tar -zcf ./build_$BUILD_NUMBER.tgz image.pex expected_sw_config.json uboot ./firmware/update.hex
