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

tar -zf ./working/image.tar ./working/image
if [$? == 0]
then
  rm -r ./working/image
fi

image_crc=`cksum ./working/image.tar | grep -o '^[[:digit:]]*'`
uboot_crc=`cksum ./working/uboot | grep -o '^[[:digit:]]*'`
mcu_update_crc=`cksum ./working/firmware/update.hex | grep -o '^[[:digit:]]*'`

jq --arg image_crc "$image_crc" \
   --arg uboot_crc "$uboot_crc" \
   --arg mcu_update_crc "$mcu_update_crc" \
   '.MCU.update.crc=$mcu_update_crc | \
   .MPC.image.crc=$image_crc | \
   .MPC.uboot.crc=$uboot_crc' \
   $sw_config > working/expected_sw_config.json /


tar -czf build_$BUILD_NUMBER.tar.gz ./working/*
