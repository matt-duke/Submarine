#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>
#include <unistd.h>

#include <hiredis-vip/hiredis.h>
#include <logger/logger.h>

#include <common.h>
#include <redis_def.h>
#include <baseapp.h>
#include "motor.h"

/* Variables */
extern const char *__progname;
redisContext *c;
redisReply *reply;

smAppClass_t state_machine;
MotorClass_t motor_l;
MotorClass_t motor_r;

/* Functions */
void do_to_init(smAppClass_t *app);
void do_to_post(smAppClass_t *app);
void do_to_fault(smAppClass_t *app);
void do_running(smAppClass_t *app);
void do_fault(smAppClass_t *app);


int main(int argc, char *argv[])
{
	init_logging();
	app_transition_table[APP_STATE_INIT][APP_STATE_INIT] = do_to_init;
	app_transition_table[APP_STATE_INIT][APP_STATE_POST] = do_to_post;
	app_transition_table[APP_STATE_INIT][APP_STATE_FAULT] = do_to_fault;
	app_transition_table[APP_STATE_RUNNING][APP_STATE_FAULT] = do_to_fault;
	app_run_table[APP_STATE_RUNNING] = do_running;
	app_run_table[APP_STATE_FAULT] = do_fault;

	appInit(&state_machine);

	while (1) {
		state_machine.run(&state_machine);
		motor_l.run(&motor_l);
		motor_r.run(&motor_r);
	}
}

void do_to_fault(smAppClass_t *app) {
	motor_l.transition(&motor_l, APP_STATE_FAULT);
	motor_r.transition(&motor_r, APP_STATE_FAULT);

	if (motor_l.state != APP_STATE_FAULT) {
		//error
	}
	if (motor_r.state != APP_STATE_FAULT) {
		//error
	}
}

void do_to_init(smAppClass_t *app) {
	if (app->state == APP_STATE_INIT) {

		pthread_t thread_id;
		pthread_create(&thread_id, NULL, heartbeatThread, (void*)__progname);
		
		init_redis(&c, REDIS_HOSTNAME, REDIS_PORT);

		motorInit(&motor_l);
		motorInit(&motor_r);
	}
}

void do_running(smAppClass_t *app) {

}


void do_fault(smAppClass_t *app) {

}