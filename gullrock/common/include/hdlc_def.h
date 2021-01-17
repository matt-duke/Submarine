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
#define PACKET_SIZE 8
#define PORT_SPEED 9600

enum HDLC_TYPE {
  HDLC_TYPE_GET = 0,
  HDLC_TYPE_SET,
  HDLC_TYPE_SUCCESS,
  HDLC_TYPE_FAILURE,
  HDLC_TYPE_NOT_IMPLEMENTED,
  HDLC_TYPE_INVALID
};

enum MCU_STATUS {
  MCU_STATUS_OK = 0,
  MCU_STATUS_POST,
  MCU_STATUS_INIT,
  MCU_STATUS_FAULT,
  MCU_NUM_STATUS
};

enum HDLC_KEYS {
  HDLC_NOT_IMPLEMENTED = 0,
  HDLC_MOTOR_SPEED,    //{16,16} (M1, M2)
  HDLC_MOTOR_CURR,     //{16,16} (M1, M2)
  HDLC_STATUS,         //{8,8,8,8} (MCU, MOTOR, NET, BATTERY)
  HDLC_FREE_MEM,       //{32}
  HDLC_CAMERA,         //{16, 16} (yaw, pitch)
  HDLC_LED,            //{32} (brightness)
  HDLC_WATER_TEMP,     //{32} (water temp)
  HDLC_TOTAL_CURR,     //{32} (current)
	HDLC_NUM_KEYS
};

typedef union Data16 {
  int16_t value;
  uint8_t bytes[2];
}data16_t;

typedef union Data32 {
  int32_t value;
  data16_t data16[2];
  uint8_t bytes[4];
}data32_t;

typedef union {
  struct {
    uint8_t type;
    uint8_t key;
    uint16_t id;
    data32_t data32;
  } s;
  uint8_t bytes[PACKET_SIZE];
} packet_t;

#ifdef __cplusplus
} 
#endif

#endif