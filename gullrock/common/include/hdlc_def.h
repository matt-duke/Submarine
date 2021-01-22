#ifndef HDLC_DEF_H
#define HDLC_DEF_H

#include <stdint.h>
#include <stdbool.h>

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
  HDLC_TYPE_NOT_IMPLEMENTED
};

typedef enum { 
    MCU_STATE_INIT = 0,
    MCU_STATE_POST,
    MCU_STATE_READY,
    MCU_STATE_FAULT,
    MCU_NUM_STATES } mcu_state_t;

enum HDLC_KEYS {
  HDLC_NOT_IMPLEMENTED = 0,
  HDLC_M1_SPEED,
  HDLC_M2_SPEED,
  HDLC_M1_CURR,
  HDLC_M2_CURR,
  HDLC_STATE,
  HDLC_NET_STATUS,
  HDLC_TEST,
  HDLC_FREE_MEM,
  HDLC_YAW,
  HDLC_PITCH,
  HDLC_LED,
  HDLC_WATER_TEMP,
  HDLC_TOTAL_CURR,
  HDLC_CRC,
  HDLC_NUM_KEYS
};

typedef union Data32 {
  int32_t i32;
  uint32_t ui32;
  float f;
  uint16_t ui16[2];
  int16_t i16[2];
  uint8_t ui8[4];
  int8_t i8[4];
  bool b[4*8];
}data32_t;

typedef union {
  struct {
    uint8_t type;
    uint8_t key;
    uint16_t id;
    data32_t d32;
  } s;
  uint8_t ui8[PACKET_SIZE];
} packet_t;

#ifdef __cplusplus
} 
#endif

#endif