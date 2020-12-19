#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>
#include <unistd.h>

#include <hiredis.h>
#include <logger.h>

#include <common.h>
#include <redis.h>
#include <baseapp.h>

//#include "light.h"
#include "imu.h"

/* Variables */
extern const char *__progname;
redisReply *reply;

ImuClass_t imu;

typedef enum status_s{
	STATUS_OK,
	STATUS_WARNING,
	STATUS_ERROR,
	STATUS_CRITICAL
} status_t;

/* Functions */
static void do_running();
static void do_post();

static status_t update_internal_sensors();
static status_t update_external_sensors();

int main(int argc, char *argv[])
{
	init_logging();

	app_run_table[APP_STATE_RUNNING] = do_running;
	app_run_table[APP_STATE_POST] = do_post;
	GlobalAppInit();
	ImuClassInit(&imu);

	while (1) {
		GlobalApp.run();
		sleep(2);
	}
}

void do_post() {
	bool result = true;
	if (0 != imu.init(&imu)) {
		result = false;
	}
	if (file_exists("./skip_post")) {
		result = true;
	}
	if (result) {
		GlobalApp.transition(APP_STATE_RUNNING);
	} else {
		GlobalApp.transition(APP_STATE_FAULT);
	}
}

void do_running() {
	if (update_internal_sensors() > STATUS_ERROR) {
		GlobalApp.transition(APP_STATE_FAULT);
	}
	if (update_external_sensors() > STATUS_ERROR) {
		GlobalApp.transition(APP_STATE_FAULT);
	}
}

static status_t update_internal_sensors() {
	return STATUS_OK;
}
static status_t update_external_sensors() {
	return STATUS_OK;
}