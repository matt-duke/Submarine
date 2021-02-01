#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>
#include <unistd.h>
#include <stdbool.h>

#include <hiredis.h>
#include <logger.h>
#include <cJSON.h>

#include <common.h>
#include <redis.h>
#include <baseapp.h>

/* Variables */
#define EX_SW_CFG "/persistent/expected_sw_config.json"
#define SKIP_POST "/persistent/skip_post"

extern const char *__progname;
redisContext *c;
redisReply *reply;

smAppClass_t state_machine;

/* Functions */
static void do_to_init(smAppClass_t *app);
static void do_to_post(smAppClass_t *app);
static void do_to_fault(smAppClass_t *app);

static void do_fault(smAppClass_t *app);

static int verify_file_config(char *filename);
static int verify_app_versions(char *filename);
static int file_crc(int *crc, char *path);
static int app_version(char *version, char *app);

int main(int argc, char *argv[]) {
	init_logging();

	app_transition_table[APP_STATE_INIT][APP_STATE_INIT] = do_to_init;
	app_transition_table[APP_STATE_INIT][APP_STATE_POST] = do_to_post;
	app_transition_table[APP_STATE_RUNNING][APP_STATE_POST] = do_to_post;
	app_transition_table[APP_STATE_FAULT][APP_STATE_POST] = do_to_post;

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
    		exit(0);
  		}
	}
  app->transition(app, APP_STATE_POST);
}

void do_to_post(smAppClass_t *app) {
	app->state = APP_STATE_POST;

	if (!file_exists(SKIP_POST)) {
		app->transition(app, APP_STATE_RUNNING);
		return;
	}

	int result = 0;
	result += verify_file_config(EX_SW_CFG);
	result += verify_app_versions(EX_SW_CFG);
	if (result != 0) {
		LOG_ERROR("POST failure");
		app->transition(app, APP_STATE_FAULT);
	} else {
		app->transition(app, APP_STATE_RUNNING);
	}
}

void do_to_fault(smAppClass_t *app) {
	app->state = APP_STATE_FAULT;

	// Redis message
}

void do_fault(smAppClass_t *app) {
	app->state = APP_STATE_FAULT;

	// Redis message
}

int verify_file_config(char *filename) {
	char *buffer;
	const cJSON *json = NULL;
	const cJSON *files = NULL;
	const cJSON *file = NULL;

	int result = 0;

	read_file(filename, &buffer);

	if (buffer) {
		cJSON *json = cJSON_Parse(buffer);
		files = cJSON_GetObjectItemCaseSensitive(json, "files");
		cJSON_ArrayForEach(file, files) {
			cJSON *crc = cJSON_GetObjectItemCaseSensitive(file, "crc");
			cJSON *path = cJSON_GetObjectItemCaseSensitive(file, "path");
			int act_crc;
			if (!file_exists(path->string)) {
				LOG_ERROR("File does not exist %s: ", path->string);
				result = 1;
			}
			else if (file_crc(&act_crc, path->string) != 0) {
				LOG_ERROR("Error getting file crc %s: ", path->string);
				result = 2;
			}
			if ((int)strtol(crc->string, NULL, 16) != act_crc) {
				LOG_ERROR("Invalid crc: %s: ", path->string);
				result = 3;
			}
		}
		cJSON_Delete(json);
	} else {
		LOG_ERROR("Empty file buffer.");
		result = 4;
	}
	free(buffer);
	return(result);
}

int verify_app_versions(char *filename) {
	char *buffer;
	const cJSON *json = NULL;
	const cJSON *apps = NULL;
	const cJSON *app = NULL;

	int result = 0;

	read_file(filename, &buffer);

	if (buffer) {
		cJSON *json = cJSON_Parse(buffer);
		apps = cJSON_GetObjectItemCaseSensitive(json, "apps");
		cJSON_ArrayForEach(app, apps) {
			cJSON *version = cJSON_GetObjectItemCaseSensitive(app, "version");
			char *act_version;
			if (app_version(act_version, app->string) != 0) {
				LOG_ERROR("Error getting app version %s: ", app->string);
				result = 2;
			}
			if (strcmp(act_version, version->string) != 0) {
				LOG_ERROR("Versions do not match: %s: ", app->string);
				result = 3;
			}
		}
		cJSON_Delete(json);
	} else {
		LOG_ERROR("Empty file buffer.");
		result = 4;
	}
	free(buffer);
	return(result);
}

int file_crc(int *crc, char *path) {
	FILE *fpipe;
    char command[10+sizeof(path)];
	sprintf(command, "crc32 %s", path);

    if (0 == (fpipe = (FILE*)popen(command, "r"))) {
        LOG_ERROR("popen() failed.");
		return(1);
    }
	fscanf(fpipe, "%x", crc);
    pclose(fpipe);
	return(0);
}

int app_version(char *version, char *app) {
	FILE *fpipe;
    char command[sizeof(app)+20];
	sprintf(command, "dpkg -l | grep %s", app);

    if (0 == (fpipe = (FILE*)popen(command, "r"))) {
        LOG_ERROR("popen() failed.");
		return(1);
    }
	char *version[100];
	if (0 == fgets(version, sizeof(version), fpipe)) {
		LOG_ERROR("Error reading result.");
		return(1);
	}
    pclose(fpipe);
	return(0);
}