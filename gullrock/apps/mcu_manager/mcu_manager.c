#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <pthread.h>

#include <hiredis-vip/hiredis.h>
#include <hiredis-vip/async.h>
#include <hiredis-vip/adapters/libevent.h>
#include <logger/logger.h>
#include <common.h>
#include <redis_def.h>
#include <baseapp.h>

#include "mcu.h"

/* Variables */
extern const char *__progname;
redisContext *c;
redisReply *reply;

<<<<<<< HEAD
McuClass_t mcu;
smAppClass_t state_machine;

/* Functions */
void do_running(smAppClass_t *app);
void do_to_init(smAppClass_t *app);
void pubsub_set(redisAsyncContext *c, void *reply, void *privdata);
void pubsub_get(redisAsyncContext *c, void *reply, void *privdata);

int main(int argc, char *argv[])
{
	init_logging();
	app_transition_table[APP_STATE_INIT][APP_STATE_INIT] = do_to_init;
	app_run_table[APP_STATE_RUNNING] = do_running;
=======
McuClass_t MCU;
smAppClass_t state_machine;

/* Functions */
void do_running_state(smAppClass_t *app);
void do_to_init_state(smAppClass_t *app);
void pubsub_set(redisAsyncContext *c, void *reply, void *privdata);
void pubsub_get(redisAsyncContext *c, void *reply, void *privdata);


void do_to_init_state(smAppClass_t *app) {
	redis_fn_callback(*pubsub_set, "pubsub_set.*");
	redis_fn_callback(*pubsub_get, "pubsub_get.*");
}

void do_running_state(smAppClass_t *app) {

}

int main(int argc, char *argv[])
{
	init_logging();
	//app_transition_table[APP_STATE_INIT][APP_STATE_INIT] = do_to_init_state;
	app_run_table[APP_STATE_RUNNING] = do_running_state;
>>>>>>> 60ea6c223e8ceaa2492ce50e09b239dee2632330

	appInit(&state_machine);

	while (1) {
		state_machine.run(&state_machine);
<<<<<<< HEAD
		mcu.run(&mcu);
	}
}

void do_to_init(smAppClass_t *app) {
	redis_fn_callback(*pubsub_set, "pubsub_set.*");
	redis_fn_callback(*pubsub_get, "pubsub_get.*");
}

void do_running(smAppClass_t *app) {

}

=======
		MCU.run(&MCU);
	}
}

>>>>>>> 60ea6c223e8ceaa2492ce50e09b239dee2632330
void pubsub_set(redisAsyncContext *c, void *reply, void *privdata) {
  redisReply *r = reply;
  if (reply == NULL) {
    LOG_DEBUG("Reply is NULL");
	return;
  }

  if (r->type == REDIS_REPLY_ARRAY) {

	if (strcmp(r->element[1]->str, "pubsub_set.io.left_motor")) {
		LOG_INFO("Setting left motor: %d", r->element[2]);
<<<<<<< HEAD
		mcu.set();
=======
>>>>>>> 60ea6c223e8ceaa2492ce50e09b239dee2632330
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

<<<<<<< HEAD
	if (strcmp(r->element[1]->str, "pubsub_get.io.motor_l")) {
		LOG_INFO("Setting left motor: %d", r->element[2]);
	} else if (strcmp(r->element[1]->str, "pubsub_set.io.motor_r")) {
=======
	if (strcmp(r->element[1]->str, "pubsub_get.io.status")) {
		LOG_INFO("Setting left motor: %d", r->element[2]);
	} else if (strcmp(r->element[1]->str, "pubsub_set.io.status")) {
>>>>>>> 60ea6c223e8ceaa2492ce50e09b239dee2632330
		LOG_INFO("Setting right motor: %d", r->element[2]);
	} else {
		LOG_DEBUG("Unrecognized channel: %s", r->element[1]->str);
	}
  }
  else {
    LOG_DEBUG("Reply of unknown type: %d", r->type);
  }
}