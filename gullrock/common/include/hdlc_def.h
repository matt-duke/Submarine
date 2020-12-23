#ifndef HDLC_DEF_H
#define HDLC_DEF_H

#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif
/*
  HDLC CONSTANTS
*/
#define MAX_HDLC_FRAME_LENGTH 64
#define PACKET_SIZE 12
#define PORT_NAME "/dev/ttyACM0"
#define PORT_SPEED 115200

enum HDLC_TYPE {
  HDLC_TYPE_GET = 0,
  HDLC_TYPE_SET,
  HDLC_TYPE_RESP
};

enum HDLC_STATUS {
  HDLC_STATUS_OK = 0,
  HDLC_STATUS_FAULT
};

typedef union Data32 {
  int32_t value;
  uint8_t bytes[sizeof(int32_t)];
}data32_t;

typedef union Data16 {
  int16_t value;
  uint8_t bytes[sizeof(int16_t)];
}data16_t;

typedef struct Packet {
  uint8_t type;
  uint16_t id;
  uint8_t key;
  data32_t data[2];
}packet_t;

typedef union Buffer {
  packet_t packet;
  uint8_t bytes[sizeof(packet_t)];
}buffer_t;

#ifdef __cplusplus
}
#endif

#endif