#ifndef COMMON_H
#define COMMON_H

#include <hiredis.h>
#include <stdbool.h>

// function prototypes
bool file_exists(char *fname);
int redis_fn_callback (void (*f)(), char *topic);
int init_redis(redisContext **c, const char *hostname, const int port);
void *heartbeatThread(void *state);
void init_logging();

#endif