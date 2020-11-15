#ifndef HDLC_H
#define HDLC_H

enum serial_commands {
  COMMAND_STATUS = 0, // 0
  COMMAND_SET_MOTOR,
  COMMAND_SET_LED,
  COMMAND_ERROR,
  COMMAND_SENSOR
};

enum status {
  STATUS_NONE = 0,
  STATUS_OK,
  STATUS_FAULT
};

const char* statusName[] = {"NONE", "OK", "FAULT"};

enum motor_id {
  ID_MOTOR_L = 0,
  ID_MOTOR_R,
  ID_HEADLIGHT,
  ID_BUILT_IN_LED
};

#endif
