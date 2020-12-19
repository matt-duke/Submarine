
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <unistd.h>
#include <pthread.h>

#include <hiredis.h>
#include <logger.h>

#include <common.h>
#include <baseapp.h>
#include <redis.h>

#define MAX_FAILURES 2

/* Variables */
extern const char *__progname;
redisContext *c;
redisReply *reply;
int failure_count;

smAppClass_t state_machine;

char* appPaths[] = {"./camera_controller", "./mcu_manager", "./motion_controller"};
char* appNames[] = {"camera_controller", "mcu_manager", "motion_controller"};

/* Functions */
void do_to_init(smAppClass_t *app);
void do_running(smAppClass_t *app);
int startApp(char* app_path);
int killApp(char* app_path);

int main() {
  init_logging();

  app_transition_table[APP_STATE_INIT][APP_STATE_INIT] = do_to_init;
  app_run_table[APP_STATE_RUNNING] = do_running;

  while (1) {
    state_machine.run(&state_machine);
  }
}

void do_to_init(smAppClass_t *app) {
	if (app->state == APP_STATE_INIT) {
	  pthread_t thread_id;
		pthread_create(&thread_id, NULL, heartbeatThread, (void*) &state_machine);
		
    failure_count = 0;

    int err = init_redis(&c, REDIS_HOSTNAME, REDIS_PORT);
		if (err != 0) {
      LOG_FATAL("Failed to init redis with error %d", err);
      abort();
    }
    for (int i=0;i<sizeof(appPaths)/sizeof(appPaths[0]); i++) {
      startApp(appPaths[i]);
    }
	}
  sleep(1);
  app.transition(&state_machine, APP_STATE_RUNNING);
}

void do_running(smAppClass_t *app) {
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
