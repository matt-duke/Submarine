#include <stdio.h>
#include <stdlib.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <pthread.h>

#include <hiredis-vip/hiredis.h>
#include <hiredis-vip/async.h>
#include <hiredis-vip/adapters/libevent.h>
#include <c-logger/logger.h>
#include <common.h>
#include <redis_def.h>
#include <baseapp.h>
#include "mcu.h"

/* Variables */
extern const char *__progname;
redisContext *c;
redisReply *reply;

McuClass_t mcu;
smAppClass_t state_machine;

/* Functions */
static void do_to_init(smAppClass_t *app);
static void do_to_fault(smAppClass_t *app);
static void do_to_post(smAppClass_t *app);
static void do_to_running(smAppClass_t *app);

static void do_fault(smAppClass_t *app);
static void do_running(smAppClass_t *app);

static void pubsub_set(redisAsyncContext *c, void *reply, void *privdata);
static void pubsub_get(redisAsyncContext *c, void *reply, void *privdata);

int main(int argc, char *argv[])
{
	init_logging();
	app_transition_table[APP_STATE_INIT][APP_STATE_INIT] = do_to_init;
	app_transition_table[APP_STATE_INIT][APP_STATE_POST] = do_to_post;
	app_transition_table[APP_STATE_POST][APP_STATE_FAULT] = do_to_fault;
	app_transition_table[APP_STATE_POST][APP_STATE_RUNNING] = do_to_running;
	app_run_table[APP_STATE_RUNNING] = do_running;
	app_run_table[APP_STATE_FAULT] = do_fault;

	appInit(&state_machine);
	mcuInit(&mcu);

	while (1) {
		state_machine.run(&state_machine);
		mcu.run(&mcu);
	}
}

void do_to_init(smAppClass_t *app) {
	if (app->state == APP_STATE_INIT) {
		pthread_t thread_id;
		pthread_create(&thread_id, NULL, heartbeatThread, (void*) &state_machine);
		
		if (init_redis(&c, REDIS_HOSTNAME, REDIS_PORT) != 0) {
    		LOG_FATAL("Failed to start.");
    		abort();
  		}
		redis_fn_callback(*pubsub_set, "pubsub_set.*");
		redis_fn_callback(*pubsub_get, "pubsub_get.*");
	}
	app.transition(&app, APP_STATE_POST);
	mcu.transition(&mcu, MCU_STATE_POST);
}

void do_to_post (smAppClass_t *app) {
	bool criteria = true;
	if (mcu.state(&mcu) != MCU_STATE_POST) {
		criteria = false;
	}
	time_t start = time(NULL);
	while (mcu.state(&mcu) == MCU_STATE_POST) {
		if (time(NULL) - start > 30) {
			criteria = false;
			break;
		}
	}
	if (!criteria) {
		app.transition(&app, APP_STATE_FAULT)
	} else {
		app.transition(&app, APP_STATE_RUNNING)
	}
}

void do_to_fault(smAppClass_t *app) {

}

void do_fault(smAppClass_t *app) {

}

void do_running(smAppClass_t *app) {
	if (mcu.state(&mcu) == MCU_STATE_FAULT) {
		app.transition(&app, APP_STATE_FAULT);
	}
}

void do_fault(smAppClass_t *app) {
	if (mcu.state(&mcu) == MCU_STATE_FAULT) {
		mcu.transition(&mcu, MCU_STATE_POST);
	} else if (mcu.state(&mcu) == MCU_STATE_FAULT) {
}

void pubsub_set(redisAsyncContext *c, void *reply, void *privdata) {
  redisReply *r = reply;
  if (reply == NULL) {
    LOG_DEBUG("Reply is NULL");
	return;
  }

  if (r->type == REDIS_REPLY_ARRAY) {

	if (strcmp(r->element[1]->str, "pubsub_set.io.left_motor")) {
		LOG_INFO("Setting left motor: %d", r->element[2]);
		//mcu.set();
	} else if (strcmp(r->element[1]->str, "pubsub_set.io.right_motor")) {
		LOG_INFO("Setting right motor: %d", r->element[2]);
	} else if (strcmp(r->element[1]->str, "pubsub_set.io.headlight")) {
		LOG_INFO("Setting headlight: %d", r->element[2]);
	} else if (strcmp(r->element[1]->str, "pubsub_set.io.lan")) {
		LOG_INFO("Setting LAN LED: %d", r->element[2]);
	} else {
		LOG_DEBUG("Unrecognized channel: %s", r->element[1]->str);
	}
  }
  else {
    LOG_DEBUG("Reply of unknown type: %d", r->type);
  }
}

void pubsub_get(redisAsyncContext *c, void *reply, void *privdata) {
  redisReply *r = reply;
  if (reply == NULL) {
    LOG_DEBUG("Reply is NULL");
	return;
  }

  if (r->type == REDIS_REPLY_ARRAY) {
	if (strcmp(r->element[1]->str, "pubsub_get.io.motor_l")) {
		LOG_INFO("Setting left motor: %d", r->element[2]);
	} else if (strcmp(r->element[1]->str, "pubsub_set.io.motor_r")) {
		LOG_INFO("Setting right motor: %d", r->element[2]);
	} else {
		LOG_DEBUG("Unrecognized channel: %s", r->element[1]->str);
	}
  }
  else {
    LOG_DEBUG("Reply of unknown type: %d", r->type);
  }
}