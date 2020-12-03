#ifndef HDLC_DEF_H
#define HDLC_DEF_H

#include <stdint.h>

/*
  HDLC CONSTANTS
*/
#define MAX_HDLC_FRAME_LENGTH 64
#define PACKET_SIZE 7
#define PORT_NAME "/dev/ttyACM0"

enum HDLC_ID {
  HDLC_GET = 0,
  HDLC_SET
};

enum HDLC_STATUS {
  HDLC_STATUS_NONE = 0,
  HDLC_STATUS_OK,
  HDLC_STATUS_FAULT
};

enum HDLC_TYPE {
  HDLC_MCU_STATUS = 0,
  HDLC_MOTOR_L,
  HDLC_MOTOR_R,
  HDLC_HEADLIGHT,
  HDLC_BUILT_IN_LED
};

typedef union Data {
  int32_t value;
  uint8_t bytes[4];
}data_t;

typedef struct Packet {
  uint8_t type;
  uint8_t id;
  uint8_t key;
  data_t data;
}packet_t;

typedef union Buffer {
  packet_t packet;
  uint8_t bytes[PACKET_SIZE];
}buffer_t;

#endif