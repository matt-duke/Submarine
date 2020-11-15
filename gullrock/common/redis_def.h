#ifndef REDIS_DEF_H
#define REDIS_DEF_H
/*
  REDIS CONSTANTS
*/

#define VALIDITY_TIMEOUT 10
#define HEARTBEAT_RATE 5
#define TIMEOUT_HEARTBEAT 5
#define REDIS_PORT 6379


enum REDIS_INIT_FAILURES {
  REDIS_CONNECTION_ERROR,
  REDIS_ALLOCARTION_FAULURE,
  REDIS_PING_FAILURE
};

extern const char* STATUS_NAME[];
extern const char *REDIS_HOSTNAME;
extern const char* CHANNEL_KEY[];

#endif
