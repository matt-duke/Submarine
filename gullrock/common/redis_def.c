#include "redis_def.h"

const char* STATUS_NAME[] = {"NONE", "OK", "FAULT"};
const char *REDIS_HOSTNAME = "127.0.0.1";
const char* CHANNEL_KEY[] = {"accel_x", "accel_y", "accel_z", "batt_volt", "current", "m_r_curr", "m_l_curr", "mcu_status"};