#ifndef REDIS_H
#define REDIS_H

#include <hiredis.h>
#include "redis_def.h"

/*
  REDIS CONSTANTS
*/

int redis_fn_callback (void (*f)(), char *topic, void *privdata);
int redis_init_context(redisContext **c);
int redis_create_keys();
int redis_add_sample(redisContext **c, char *key, double value);

#endif
