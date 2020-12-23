#ifndef REDIS_DEF_H
#define REDIS_DEF_H

#ifdef __cplusplus
extern "C" {
#endif

#define VALIDITY_TIMEOUT 10
#define TIMEOUT_HEARTBEAT 10
#define HEARTBEAT_RATE 5
#define REDIS_HOSTNAME "127.0.0.1"
#define REDIS_PORT 6379

enum REDIS_KEY_ID {
	KEY_ACCEL_X,
	KEY_ACCEL_Y,
	KEY_ACCEL_Z,
  KEY_MPC_CPU_TEMP,
  KEY_MPC_UNDER_VOLT,
  KEY_MPC_THROTTLED,
  KEY_MPC_SOFT_TEMP_LIMIT,
  KEY_MPC_THROTTLED,
	REDIS_NUM_KEYS
};

typedef enum REDIS_INIT_FAILURES {
  REDIS_CONNECTION_ERROR,
  REDIS_ALLOCATION_FAULURE,
  REDIS_PING_FAILURE
} redis_fail_t;

typedef struct redis_key_s{
  char* name;
  int retention;
} redis_key_t;

extern redis_key_t REDIS_KEYS[];

void InitKeys();

#ifdef __cplusplus
}
#endif
#endif