#ifndef REDIS_H
#define REDIS_H

#include <hiredis.h>
#include <stdbool.h>

#define VALIDITY_TIMEOUT 10
#define TIMEOUT_HEARTBEAT 10
#define HEARTBEAT_RATE 5
#define REDIS_HOSTNAME "127.0.0.1"
#define REDIS_PORT 6379

enum REDIS_KEY {
    REDIS_ACCEL_X,
    REDIS_ACCEL_Y,
    REDIS_ACCEL_Z,
    REDIS_M1_SPEED,
    REDIS_M2_SPEED,
    REDIS_M1_CURR,
    REDIS_M2_CURR,
    REDIS_CAM_STATUS
    REDIS_WATER_TEMP,
    REDIS_TOTAL_CURR,
    REDIS_HEADLIGHT,
    REDIS_MPC_NET_STATUS,
    REDIS_MCU_STATE,
    REDIS_MCU_FREE_MEM,
    REDIS_MPC_CPU_TEMP,
    REDIS_MPC_CPU_IDLE,
    REDIS_MPC_LOAD_AVG_1MIN,
    REDIS_MPC_LOAD_AVG_5MIN,
    REDIS_MPC_LOAD_AVG_15MIN,
    REDIS_MPC_VOLTS,
    REDIS_MPC_UNDER_VOLT,
    REDIS_MPC_FREQ_CAP,
    REDIS_MPC_THROTTLED,
    REDIS_MPC_SOFT_TEMP_LIMIT,
    REDIS_NUM_KEYS
};

typedef enum redis_init_failures_s {
    REDIS_CONNECTION_ERROR,
    REDIS_ALLOCATION_FAULURE,
    REDIS_PING_FAILURE
} redis_fail_t;

typedef struct redis_label_s {
    char *units;
} redis_label_t;

typedef struct redis_key_s {
    char *key;
    int retention;
    bool ts;
    int type;
    int hdlc_key;
    int hdlc_index;
    //redis_label_t labels;
} redis_key_t;

extern redis_key_t REDIS_KEYS[];

// FUNCTIONS
void redis_init_keys();
int redis_create_keys(redisContext **c);

int redis_fn_callback(void (*f)(), char *topic, void *privdata);
int redis_init_context(redisContext **c);
void push_to_redis(redisContext *c, int i, void *data);

#endif
