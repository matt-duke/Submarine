# install dependencies
apt install libssl-dev
apt install dh-autoreconf

# Build libserialport from source
chmod +x gullrock/libs/libserialport/autogen.sh
gullrock/libs/libserialport/autogen.sh
gullrock/libs/libserialport/configure
make -C gullrock/libs/libserialport install

# Build libevent from source
chmod +x gullrock/libs/libevent/autogen.sh
gullrock/libs/libevent/autogen.sh
gullrock/libs/libevent/configure
make -C gullrock/libs/libevent install

# Build hiredis-vip from source
make -C gullrock/libs/hiredis-vip install
