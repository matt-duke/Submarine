#include <stdio.h>
#include <stdlib.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <pthread.h>
#include <hiredis.h>
#include <async.h>
#include <logger.h>

#include <common.h>
#include <redis.h>
#include <baseapp.h>
#include "mcu.h"

/* Variables */
extern const char *__progname;

McuClass_t mcu;

/* Functions */

static void do_init();
static void do_post();
static void do_running();
static void do_fault();

static void pubsub_set(redisAsyncContext *c, void *reply, void *privdata);
static void pubsub_get(redisAsyncContext *c, void *reply, void *privdata);

int main(int argc, char *argv[])
{
	init_logging();

	app_transition_table[APP_STATE_POST][APP_STATE_RUNNING] = do_to_running;
	app_run_table[APP_STATE_INIT] = do_init;
	app_run_table[APP_STATE_POST] = do_post;
	app_run_table[APP_STATE_RUNNING] = do_running;
	app_run_table[APP_STATE_FAULT] = do_fault;

	GlobalAppInit();
	mcuInit(&mcu);

	while (1) {
		state_machine.run(&state_machine);
		mcu.run(&mcu);
	}
}

void do_init() {
	GlobalApp.transition(APP_STATE_POST);
	mcu.transition(&mcu, MCU_STATE_POST);
}

void do_to_post () {
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
		GlobalApp.transition(APP_STATE_FAULT);
	} else {
		GlobalApp.transition(APP_STATE_RUNNING);
	}
}

void do_running() {
	if (mcu.state(&mcu) == MCU_STATE_FAULT) {
		GlobalApp.transition(APP_STATE_FAULT);
	}
}

void do_fault() {
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