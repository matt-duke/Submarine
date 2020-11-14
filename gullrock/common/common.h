#ifndef COMMON_H
#define COMMON_H

#include <hiredis-vip/hiredis.h>
#include <pthread.h>

// function prototypes
int redis_fn_callback (void (*f)(), char *topic);
pthread_mutex_t init_redis(redisContext **c, const char *hostname, const int port);
void *heartbeatThread(void *state);
void init_logging();

#endif