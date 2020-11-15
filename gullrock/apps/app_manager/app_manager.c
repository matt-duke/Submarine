
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <unistd.h>
#include <pthread.h>

#include <hiredis-vip/hiredis.h>
#include <logger/logger.h>

#include <common.h>
#include <definitions.h>

#define MAX_FAILURES 2

extern const char *__progname;
redisContext *c;
redisReply *reply;
pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;

/*
TODO: Change app paths
*/
char* appPaths[] = {"./camera_controller", "./mcu_manager", "./motion_controller"};
char* appNames[] = {"camera_controller", "mcu_manager", "motion_controller"};


int startApp(char* app_path) {
  LOG_INFO("Starting app %s\n", app_path);
  char cmd[128];
  sprintf(cmd, "%s &", app_path);
  int status = system(cmd);
  if (status != 0) {
    LOG_ERROR("Failed to start %s with exit code %d.\n", app_path, status / 256);
  }
  return(status/256);
}

int killApp(char* app_name) {
  LOG_INFO("Killing processes with name %s\n", app_name);
  char cmd[128];
  sprintf(cmd, "killall %s", app_name);
  int status = system(cmd);
  if (status != 0) {
    LOG_ERROR("Failed to kill %s with exit code %d.\n", app_name, status / 256);
  }
  return (status/256);
}


int main() {
  init_logging();

  killApp("redis-server");
  startApp("redis-server");

  sleep(1);

  mutex = init_redis(&c, REDIS_HOSTNAME, REDIS_PORT);

  for (int i=0; i<sizeof(appPaths)/sizeof(appPaths[0]); i++ ) {
    startApp(appPaths[i]);
  }

  sleep(1);

  int failure_count = 0;

  while (1) {
    for (int i = 0; i < sizeof(appNames)/sizeof(appNames[0]); i++) {
      reply = redisCommand(c,"TTL %s", appNames[i]);

      if (reply->type != REDIS_REPLY_INTEGER) {
        LOG_ERROR("TTL error, reply is not an integer.\n");
        abort();
      }

      switch (reply->integer) {
        case -2:
          LOG_ERROR("Heartbeat failed (expired) Restarting app: %s\n", appNames[i]);
          killApp(appNames[i]);
          startApp(appPaths[i]);
          failure_count++;
          break;
        case -1:
          LOG_ERROR("Heartbeat failed (no expiry). Error in SET: %s\n", appNames[i]);
          failure_count++;
          break;
        default:
          LOG_DEBUG("TTL REPLY %s %lld\n", appNames[i], reply->integer);
          break;
      }
      freeReplyObject(reply);
    }
    if (failure_count > MAX_FAILURES) {
      LOG_FATAL("Exceeded max app crash failures. Aborting.\n");
      abort();
    }
    sleep(HEARTBEAT_RATE);
  }
}
