#include "redis_def.h"

#define redis_key_default {"null", 2000}
redis_key_t REDIS_KEYS[] = {[0 ... REDIS_NUM_KEYS] = redis_key_default };

void InitKeys() {
    REDIS_KEYS[REDIS_KEY_ACCEL_X].name = "accel_x";
	REDIS_KEYS[REDIS_KEY_ACCEL_Y].name = "accel_y";
	REDIS_KEYS[REDIS_KEY_ACCEL_Z].name = "accel_z";
	REDIS_KEYS[REDIS_KEY_CPU_TEMP].name = "cpu_temp";
}