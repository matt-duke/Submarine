#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>
#include <unistd.h>

#include <hiredis.h>
#include <logger.h>

#include <common.h>
#include <redis_def.h>
#include <baseapp.h>

#include "camera.h"

/* Variables */
extern const char *__progname;
redisContext *c;
redisReply *reply;

smAppClass_t state_machine;
CameraClass_t camera;

/* Functions */
static void do_to_init(smAppClass_t *app);
static void do_post(smAppClass_t *app);
static void do_running(smAppClass_t *app);

int main(int argc, char *argv[])
{
	init_logging();
	app_transition_table[APP_STATE_INIT][APP_STATE_INIT] = do_to_init;
	app_run_table[APP_STATE_RUNNING] = do_running;

	appInit(&state_machine);

	while (1) {
		state_machine.run(&state_machine);

	}
}

void do_to_init(smAppClass_t *app) {
	if (app->state == APP_STATE_INIT) {
		pthread_t thread_id;
		pthread_create(&thread_id, NULL, heartbeatThread, (void*) &state_machine);
		
		if (init_redis(&c, REDIS_HOSTNAME, REDIS_PORT) != 0) {
    		LOG_FATAL("Failed to start.");
    		exit(1);
  		}
	}
  app->transition(app, APP_STATE_RUNNING);
}

void do_post(smAppClass_t *app) {
	if (camera.state == CAMERA_STATE_POST) {
		return;
	} else if (false) {
		//mcu state post
	} else {
		app->transition(app, APP_STATE_RUNNING);
	}
}


void do_running(smAppClass_t *app) {
	if (camera.state == CAMERA_STATE_FAULT) {
		app->transition(app, APP_STATE_FAULT);
	}
}