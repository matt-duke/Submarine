
ARDUNIO_CLI=bin/arduino-cli
CORE=arduino:avr
FQBN=arduino:avr:mega
BUILD_DIR=build
COMMON=$(readlink -f ../../common/)
LIB_DIR=$(readlink -f ../libraries/)

FAST=false

while getopts ":f" opt; do
  case $opt in
    f)
      echo "Runnning in fast mode" >&2
      FAST=true
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
  esac
done

if [ -f "$ARDUNIO_CLI" ]; then
    echo "$ARDUNIO_CLI exists."
else
    echo "Downloading $ARDUNIO_CLI..."
    curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | sh
    $ARDUNIO_CLI core update-index
fi

if [ "$FAST" = false ]; then
    $ARDUNIO_CLI lib install "FreeRTOS"
    $ARDUNIO_CLI lib install "Adafruit NeoPixel"
    $ARDUNIO_CLI lib install "Servo Hardware PWM"
    $ARDUNIO_CLI lib install "CircularBuffer"
    $ARDUNIO_CLI lib install --git-url https://github.com/mengguang/ArduinoHDLC.git
    #$ARDUNIO_CLI lib install --git-url https://github.com/sparkfun/SparkFun_TB6612FNG_Arduino_Library.git
    $ARDUNIO_CLI lib install --git-url https://github.com/mpflaga/Arduino-MemoryFree.git

    if echo "arduino-cli core list" | grep -q "$CORE" ; then
        echo "$CORE already installed"
    else
        $ARDUNIO_CLI core install $CORE
    fi
fi

mkdir -p $BUILD_DIR

rm -f $COMMON_ZIP && rm -rf $BUILD_DIR/Arduino/libraries/common && rm -rf $BUILD_DIR/common
FILE_LIST="$COMMON/src/hdlc_def.c $COMMON/include/hdlc_def.h"
mkdir $BUILD_DIR/common
cp $FILE_LIST $BUILD_DIR/common/
(cd $BUILD_DIR && zip -r common.zip common)
$ARDUNIO_CLI lib install --zip-path $BUILD_DIR/common.zip

for dir in $LIB_DIR/* ; do
    if [ -d "$dir" ]; then
        lib_name=$(basename $dir)
        zip=$lib_name.zip
        rm -f $BUILD_DIR/$zip && rm -rf $BUILD_DIR/$lib_name && rm -rf $BUILD_DIR/Arduino/libraries/$lib_name
        cp -r $dir $BUILD_DIR/$lib_name
        (cd $BUILD_DIR && zip -r $zip $lib_name)

        #$ARDUNIO_CLI lib uninstall $lib_name
        $ARDUNIO_CLI lib install --zip-path $BUILD_DIR/$zip
    fi
done