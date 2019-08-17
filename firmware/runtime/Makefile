ARDUINO_DIR  = /usr/share/arduino
BOARD_TAG    = mega2560
ARDUINO_PORT = /dev/ttyACM0
ARDUINO_LIBS = EventManager EEPROM
USER_LIB_PATH := $(shell dirname $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST)))))/libraries

include /usr/share/arduino/Arduino.mk
