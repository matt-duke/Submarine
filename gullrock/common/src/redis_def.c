#include "redis_def.h"

#define redis_key_default {"null", 2000}
redis_key_t REDIS_KEYS[] = {[0 ... REDIS_NUM_KEYS] = redis_key_default };

void InitKeys() {
    REDIS_KEYS[KEY_ACCEL_X].name = "accel_x";
	REDIS_KEYS[KEY_ACCEL_Y].name = "accel_y";
	REDIS_KEYS[KEY_ACCEL_Z].name = "accel_z";
	REDIS_KEYS[KEY_MCU_STATUS].name = "mcu_status";
	REDIS_KEYS[KEY_MCU_FREE_MEM].name = "mcu_free_mem";
	#ifndef __cplusplus
	REDIS_KEYS[KEY_MPC_CPU_TEMP].name = "mpc_cpu_temp";
	REDIS_KEYS[KEY_MPC_UNDER_VOLT].name = "mpc_under_volt";
	REDIS_KEYS[KEY_MPC_FREQ_CAP].name = "mpc_freq_cap";
	REDIS_KEYS[KEY_MPC_THROTTLED].name = "mpc_throttled";
	REDIS_KEYS[KEY_MPC_SOFT_TEMP_LIMIT].name = "mpc_soft_temp_limit";
	#endif
}