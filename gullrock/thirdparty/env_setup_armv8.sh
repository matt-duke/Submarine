#!/usr/bin/env bash

set -ex

export RPI_TOOLCHAIN_DIR=/home/matt/GitHub/RPi-Cpp-Toolchain
export RPI_SYSROOT=$RPI_TOOLCHAIN_DIR/toolchain/sysroot-armv8-rpi3-linux-gnueabihf
export TOOLCHAIN_BIN=$RPI_TOOLCHAIN_DIR/toolchain/x-tools/armv8-rpi3-linux-gnueabihf/bin
export CC=$TOOLCHAIN_BIN/armv8-rpi3-linux-gnueabihf-gcc
export CXX=$TOOLCHAIN_BIN/armv8-rpi3-linux-gnueabihf-g++
source $RPI_TOOLCHAIN_DIR/toolchain/docker/merged/env/armv8-rpi3-linux-gnueabihf.env
source $RPI_TOOLCHAIN_DIR/toolchain/docker/merged/cross-build/tools/cross-pkg-config