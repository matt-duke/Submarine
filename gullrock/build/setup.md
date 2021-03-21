# Building
## Cross Compiling
http://amgaera.github.io/blog/2014/04/10/cross-compiling-for-raspberry-pi-on-64-bit-linux/
https://stackoverflow.com/questions/19162072/how-to-install-the-raspberry-pi-cross-compiler-on-my-linux-host-machine/58559140#58559140

autoreconf
libtool
gcc
g++

# Dependecies
## GSTREAMER
gir1.2-gst-plugins-base-1.0 -- for GstVideo (not needed?)

gstreamer1.0-libav

## REDIS
wget http://download.redis.io/redis-stable.tar.gz
tar xvzf redis-stable.tar.gz
cd redis-stable
make

git clone git://git.drogon.net/wiringPi
$ cd wiringPi
$ ./build

## REDIS C LIBRARY
hiredis-vip
make -> generates libhiredis_vip.so
copy to /usr/lib
update using sudo ldconfig
check with sudo ldconfig -p | grep redis


## SERIAL LIBRARY
git clone https://github.com/sigrokproject/libserialport.git
install dh-autoreconf
run autogen.sh, then configure.sh
make install
ldconfig

## GST_RPICAM
#https://github.com/thaytan/gst-rpicamsrc/
sudo apt install libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev
git clone https://github.com/thaytan/gst-rpicamsrc.git
cd gst-rpicamsrc
./autogen.sh
make
sudo make install

## Disable BT to use UART (PL011)
https://scribles.net/disabling-bluetooth-on-raspberry-pi/
https://www.raspberrypi.org/documentation/configuration/uart.md
