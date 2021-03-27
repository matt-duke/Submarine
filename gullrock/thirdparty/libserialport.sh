#!/usr/bin/env bash

set -ex

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Configure
pushd $DIR/libserialport
source ../env_setup_armv8.sh

./autogen.sh
./configure \
    --host="${HOST_TRIPLE}" \
    --prefix=$1 \
    --with-sysroot="${RPI_SYSROOT}" \
    --enable-static=yes \
    --disable-shared

# Build
make -j$(($(nproc) * 2))

# Install
#make install DESTDIR="${RPI_SYSROOT}"

# Cleanup
popd
