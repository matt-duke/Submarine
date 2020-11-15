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
#include <definitions.h>

/* Variables */
extern const char *__progname;
redisContext *c;
redisReply *reply;
smAppClass_t state_machine;

/* Functions */
void do_to_init(smAppClass_t *app);
void do_to_running(smAppClass_t *app);

int main() {
  init_logging();
  
	LOG_INFO("Starting %s", __progname);
  pthread_t thread_id;
  pthread_create(&thread_id, NULL, heartbeatThread, (void*)__progname);

  mutex = init_redis(&c, REDIS_HOSTNAME, REDIS_PORT);

  //initStream();

  while (1) {
    sleep(1);
  }
}


