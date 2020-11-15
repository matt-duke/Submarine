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

#include "light.h"
#include "imu.h"

/* Variables */
extern const char *__progname;
redisContext *c;
redisReply *reply;
pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;

smAppClass_t state_machine;
ImuClass_t imu;
LightClass_t light;

/* Functions */

void do_to_init(smAppClass_t *app);
void do_running(smAppClass_t *app);
void do_to_fault(smAppClass_t *app);
void do_fault(smAppClass_t *app);

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
		
		init_redis(&c, REDIS_HOSTNAME, REDIS_PORT);

		imuClassInit(&imu);
	}
}

void do_to_fault(smAppClass_t *app) {

}

void do_fault(smAppClass_t *app) {

}

void do_running(smAppClass_t *app) {
	
}