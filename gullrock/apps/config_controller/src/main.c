#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>
#include <unistd.h>
#include <stdbool.h>

#include <hiredis.h>
#include <logger.h>

#include <jsmn.h>

#include <common.h>
#include <redis_def.h>
#include <baseapp.h>

/* Variables */
#define SCHEMA_DIR "/config/schema"
#define DB_DIR "/config/db"

extern const char *__progname;
redisContext *c;
redisReply *reply;
jsmn_parser parser;
jsmntok_t tokens[10];

smAppClass_t state_machine;

/* Functions */
static void do_to_init(smAppClass_t *app);
static void do_to_post(smAppClass_t *app);

static void do_fault(smAppClass_t *app);
static void do_running(smAppClass_t *app);

static int file_crc(int *crc, char *path);

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
    		abort();
  		}
	}
  app->transition(app, APP_STATE_POST);
}

static void do_running(smAppClass_t *app) {

}

/*static void do_to_post(smAppClass_t *app) {
	LOG_INFO("Verifying files: FILE_PATHS");
	bool criteria = true;
	for (int i = 0; i < sizeof(FILE_PATHS); i++) {
		char *file = basename(FILE_PATHS[i]);
		int crc;
		if (!exists(FILE_PATHS[i])) {
			LOG_ERROR("File missing %s", file);
			criteria = false;
		}
		else if (0 != get_file_crc(crc, FILE_PATHS[i])) {
			LOG_ERROR("CRC validation failed for %s", file);
			criteria = false;
		}
		if (!criteria) {
			app->transition(app, APP_STATE_FAULT);
		} else {
			app->transition(app, APP_STATE_RUNNING);
		}
	}
}*/

int read_file_crc(char *filename) {
	char * buffer = 0;
	long length;
	FILE * f = fopen (filename, "rb");

	if (f) {
		fseek (f, 0, SEEK_END);
		length = ftell (f);
		fseek (f, 0, SEEK_SET);
		buffer = malloc(length);
		if (buffer) {
			fread (buffer, 1, length, f);
		}
		fclose (f);
	}
	if (buffer) {
		jsmn_init(&parser);
		jsmn_parse(&parser, buffer, strlen(buffer), tokens, 10);
	}
}

int file_crc(int *crc, char *path) {
	FILE *fpipe;
    char command[10+sizeof(path)];
	sprintf(command, "crc32 %s", path);

    if (0 == (fpipe = (FILE*)popen(command, "r")))
    {
        LOG_ERROR("popen() failed.");
		return(1);
    }
	fscanf(fpipe, "%x", crc);
    pclose(fpipe);
	return(0);
}