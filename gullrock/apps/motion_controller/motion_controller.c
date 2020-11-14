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

extern const char *__progname;
redisContext *c;
redisReply *reply;
pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;

smAppClass_t state_machine;
MotorClass_t motor_l;
MotorClass_t motor_r;

void transition_to_init_state(smAppClass_t *app) {
	if (app->curr_state == APP_STATE_INIT) {

		pthread_t thread_id;
		pthread_create(&thread_id, NULL, heartbeatThread, (void*)__progname);
		
		mutex = init_redis(&c, REDIS_HOSTNAME, REDIS_PORT);

		motorInit(&motor_l);
		motorInit(&motor_r);
	}
}

void do_running_state(smAppClass_t *app) {

}

void do_transition_to_fault_state(smAppClass_t *app) {
	motor_l.transition(&motor_l, APP_STATE_FAULT);
	motor_r.transition(&motor_r, APP_STATE_FAULT);

	if (motor_l.curr_state != APP_STATE_FAULT) {
		//error
	}
	if (motor_r.curr_state != APP_STATE_FAULT) {
		//error
	}
}

void do_fault_state(smAppClass_t *app) {

}

int main(int argc, char *argv[])
{
	init_logging();
	//app_transition_table[APP_STATE_INIT][APP_STATE_INIT] = transition_to_init_state;
	app_transition_table[APP_STATE_INIT][APP_STATE_FAULT] = do_transition_to_fault_state;
	app_transition_table[APP_STATE_RUNNING][APP_STATE_FAULT] = do_transition_to_fault_state;

	app_run_table[APP_STATE_RUNNING] = do_running_state;
	app_run_table[APP_STATE_FAULT] = do_fault_state;

	appInit(&state_machine);

	while (1) {
		state_machine.run(&state_machine);
		motor_l.run(&motor_l);
		motor_r.run(&motor_r);


	}
}