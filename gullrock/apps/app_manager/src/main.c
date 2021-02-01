
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>

#include <hiredis.h>
#include <logger.h>

#include <common.h>
#include <baseapp.h>
#include <redis.h>

#define MAX_FAILURES 2

/* Variables */
extern const char *__progname;

#define APP_DIR "/apps"
#define START_REDIS "redis-server /persistent/redis.conf"

#define NUM_APPS 5
char* appNames[NUM_APPS] = {
  "camera_controller",
  "mcu_manager",
  "motion_controller",
  "io_controller",
  "config_controller"
};

/* Functions */
static void do_to_init();
static void do_post();
static void do_running();
static void do_test();

static int monitor_heartbeats(char *app_name);
static int start_app(char* app_name);
static int kill_app(char* app_name);

int main() {
  #ifdef TEST
  run_test(); 
  #else
  init_logging();
  app_transition_table[APP_STATE_INIT][APP_STATE_INIT] = do_to_init;
  app_run_table[APP_STATE_POST] = do_post;
  app_run_table[APP_STATE_RUNNING] = do_running;

  GlobalAppInit();

  while (1) {
    GlobalApp.run();
  }
  #endif
}

void do_to_init() {
  // TODO: Move starting redis server to startup script
  char buffer[128];
  if (run_cmd(buffer, START_REDIS) != 0) {
    LOG_ERROR("Error starting redis server");
    GlobalApp.transition(APP_STATE_FAULT);
    return;
  } else {
    for (int i=0; i<NUM_APPS;i++) {
      start_app(appNames[i]);
    }
  }
}

void do_post() {
  bool any_in_post = false;
  bool any_in_fault = false;
  for (int i; i<NUM_APPS;i++) {
    int state = monitor_heartbeats(appNames[i]);
    if (state == APP_STATE_FAULT) {
      LOG_ERROR("%s in fault state.", appNames[i]);
      any_in_fault = true;
    } else if (state == APP_STATE_POST) {
      any_in_post = true;
    }
  }
  if (any_in_fault) {
    GlobalApp.transition(APP_STATE_FAULT); return;
  } else if (!any_in_post) {
    GlobalApp.transition(APP_STATE_RUNNING); return;
  }
}

void do_running() {
  bool any_in_fault = false;
  for (int i; i<NUM_APPS;i++) {
    int state = monitor_heartbeats(appNames[i]);
    if (state == APP_STATE_FAULT) {
      LOG_ERROR("%s in fault state.", appNames[i]);
      any_in_fault = true;
    }
  }
  if (any_in_fault) {
    GlobalApp.transition(APP_STATE_FAULT); return;
  }
}

int monitor_heartbeats(char *app_name) {
  redisReply *reply = redisCommand(GlobalApp.context,"TTL %s", app_name);
  if (reply->type != REDIS_REPLY_INTEGER) {
    LOG_ERROR("TTL error, reply is not an integer.");
    return -1;
  } else {
    switch (reply->integer) {
      case -2:
        LOG_ERROR("Heartbeat failed (expired): %s", app_name);
        return -1;
        break;
      case -1:
        LOG_ERROR("Heartbeat failed (no expiry). Error in SET: %s", app_name);
        return -1;
        break;
      default:
        LOG_DEBUG("TTL REPLY %s %lld", app_name, reply->integer);
        reply = redisCommand(GlobalApp.context,"GET %s", app_name);
        if (reply->type != REDIS_REPLY_INTEGER) {
          LOG_ERROR("TTL error, reply is not an integer.");
          return -1;
        } else {
          return reply->integer;
        }
    }
  }
  freeReplyObject(reply);
}

int start_app(char* app_name) {
  LOG_INFO("Starting app %s", app_name);
  char cmd[256];
  sprintf(cmd, APP_DIR"/%s &", app_name);
  int status = system(cmd);
  if (status != 0) {
    LOG_ERROR("Failed to start %s with exit code %d.", app_name, status / 256);
  }
  return(status/256);
}

int kill_app(char* app_name) {
  LOG_INFO("Killing processes with name %s", app_name);
  char cmd[128];
  sprintf(cmd, "killall %s", app_name);
  int status = system(cmd);
  if (status != 0) {
    LOG_ERROR("Failed to kill %s with exit code %d.", app_name, status / 256);
  }
  return (status/256);
}
