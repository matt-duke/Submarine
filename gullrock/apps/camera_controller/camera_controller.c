#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <unistd.h>
#include <pthread.h>

#include <hiredis-vip/hiredis.h>
#include <hiredis-vip/async.h>
#include <hiredis-vip/adapters/libevent.h>
#include <logger/logger.h>

#include <common.h>
#include <redis_def.h>

/* Variables */
extern const char *__progname;
redisContext *c;
redisReply *reply;

/* Functions */


int main() {
  init_logging();
  
	LOG_INFO("Starting %s", __progname);
  pthread_t thread_id;
  pthread_create(&thread_id, NULL, heartbeatThread, (void*) &state_machine);

  if (init_redis(&c, REDIS_HOSTNAME, REDIS_PORT) != 0) {
    LOG_FATAL("Failed to start.");
    abort();
  }

  //initStream();

  while (1) {
    sleep(1);
  }
}
