#ifndef REDIS_H
#define REDIS_H

#define CHANNEL_SET_MOTOR_L set_motor_l
#define CHANNEL_SET_MOTOR_R set_motor_r
#define CHANNEL_SET_HEADLIGHT set_headlight


enum sensor_keys {
  SENSOR_ACCEL_X,
  SENSOR_ACCEL_Y,
  SENSOR_ACCEL_Z,
  SENSOR_BATT_VOLT,
  SENSOR_CURRENT,
  SENSOR_MOTOR_L_CURR,
  SENSOR_MOTOR_R_CURR
};

const char* sensorKey[] = {"accel_x", "accel_y", "accel_z", "batt_volt", "current", "motor_r_curr", "motor_l_curr"};

#endif
