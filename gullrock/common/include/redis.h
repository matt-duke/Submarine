#ifndef REDIS_H
#define REDIS_H

#include <hiredis.h>

/*
  REDIS CONSTANTS
*/

#define VALIDITY_TIMEOUT 10
#define TIMEOUT_HEARTBEAT 10
#define HEARTBEAT_RATE 5
#define REDIS_HOSTNAME "127.0.0.1"
#define REDIS_PORT 6379

enum REDIS_KEY_ID {
	REDIS_KEY_ACCEL_X,
	REDIS_KEY_ACCEL_Y,
	REDIS_KEY_ACCEL_Z,
  REDIS_KEY_CPU_TEMP,
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

int redis_fn_callback (void (*f)(), char *topic, void *privdata);
int redis_init_context(redisContext **c);
int redis_create_keys();

#endif
