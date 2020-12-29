
ARDUNIO_CLI=bin/arduino-cli
CORE=arduino:avr
FQBN=arduino:avr:mega
BUILD_DIR=build
COMMON=$(readlink -f ../../common/)
COMMON_ZIP=$(readlink -f $BUILD_DIR/common.zip)

if [ -f "$ARDUNIO_CLI" ]; then
    echo "$ARDUNIO_CLI exists."
else
    echo "Downloading $ARDUNIO_CLI..."
    curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | sh
    $ARDUNIO_CLI core update-index
fi

rm $COMMON_ZIP && rm -r $BUILD_DIR/Arduino/libraries/common && rm -r $BUILD_DIR/common

FILE_LIST="$COMMON/src/redis_def.c $COMMON/include/redis_def.h $COMMON/src/hdlc_def.c $COMMON/include/hdlc_def.h"
mkdir $BUILD_DIR/common
cp $FILE_LIST $BUILD_DIR/common/
(cd $BUILD_DIR && zip -r $COMMON_ZIP common/*)

$ARDUNIO_CLI lib install FreeRTOS
$ARDUNIO_CLI lib install DualMC33926MotorShield
$ARDUNIO_CLI lib install --git-url https://github.com/mengguang/ArduinoHDLC.git
$ARDUNIO_CLI lib install --git-url https://github.com/sparkfun/SparkFun_TB6612FNG_Arduino_Library.git
$ARDUNIO_CLI lib install --git-url https://github.com/mpflaga/Arduino-MemoryFree.git
$ARDUNIO_CLI lib install --zip-path $COMMON_ZIP

if echo "arduino-cli core list" | grep -q "$CORE" ; then
    echo "$CORE already installed"
else
    $ARDUNIO_CLI core install $CORE
fi