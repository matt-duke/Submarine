#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <signal.h>
#include <pthread.h>
#include <stdbool.h>

#include <logger.h>
#include <hiredis.h>
#include <async.h>
#include <adapters/libevent.h>

#include "redis_def.h"
#include "baseapp.h"
#include "common.h"

/* Variables */
extern const char *__progname;

int run_cmd(char **cmd, char **output) {
	FILE *fpipe;

    if (0 == (fpipe = (FILE*)popen(*cmd, "r"))) {
		LOG_ERROR("popen() failed.");
		pclose(fpipe);
		return(1);
    }
	if (0 == fgets(*output, sizeof(*output), fpipe)) {
		LOG_ERROR("Error reading result.");
		pclose(fpipe);
		return(2);
	}
    pclose(fpipe);
	return(0);
}

int read_file(char* filename, char **buffer) {
	LOG_DEBUG("Reading %s", filename);
	FILE *fp = fopen (filename, "rb");

	if (fp != NULL) {
		/* Go to the end of the file. */
		if (fseek(fp, 0L, SEEK_END) == 0) {
			/* Get the size of the file. */
			long bufsize = ftell(fp);
			if (bufsize == -1) { /* Error */ }

			/* Allocate our buffer to that size. */
			*buffer = malloc(sizeof(char) * (bufsize + 1));
			/* Go back to the start of the file. */
			if (fseek(fp, 0L, SEEK_SET) != 0) { /* Error */ }

			/* Read the entire file into memory. */
			size_t newLen = fread(*buffer, sizeof(char), bufsize, fp);
			if ( ferror( fp ) != 0 ) {
				LOG_ERROR("Error reading file");
			} else {
				(*buffer)[newLen++] = '\0'; /* Just to be safe. */
			}
		}
		fclose(fp);
	}
}

bool file_exists(char *fname) {
	if(access( fname, F_OK ) != -1) {
		return true;
	} else {
		return false;
	}
}

char* concat(const char *s1, const char *s2) {
    char *result = malloc(strlen(s1) + strlen(s2) + 1); // +1 for the null-terminator
    if (result == NULL) {
		LOG_FATAL("Failed to malloc on concat");
		exit(1);
	}
    strcpy(result, s1);
    strcat(result, s2);
    return result;
}

int redis_fn_callback (void (*f)(), char *topic) {
    signal(SIGPIPE, SIG_IGN);
    struct event_base *base = event_base_new();

    redisAsyncContext *c = redisAsyncConnect(REDIS_HOSTNAME, REDIS_PORT);
    if (c->err) {
        LOG_ERROR("error: %s\n", c->errstr);
        return 1;
    }

    redisLibeventAttach(c, base);
	char cmd[100];
	if (strstr(topic, "*") != NULL) {
		sprintf(cmd, "PSUBSCRIBE %s", topic);
	} else {
		sprintf(cmd, "SUBSCRIBE %s", topic);
	}
    int result = redisAsyncCommand(c, f, NULL, cmd);
    event_base_dispatch(base);
	return result;
}

int init_redis(redisContext **c, const char *hostname, const int port) {
	struct timeval timeout = { 1, 500000 };

  	redisReply *reply;
	*c = redisConnectWithTimeout(hostname, port, timeout);
	if (c == NULL || (*c)->err) {
		if (c) {
				LOG_ERROR("Connection error: %s\n", (*c)->errstr);
				redisFree(*c);
				return REDIS_CONNECTION_ERROR;
		} else {
				LOG_ERROR("Connection error: can't allocate redis context\n");
				redisFree(*c);
				return REDIS_ALLOCARTION_FAULURE;
		}
	}
	reply = redisCommand(*c,"PING");
	if (strcmp(reply->str, "PONG")) {
		LOG_ERROR("Failed to ping Redis server. Replied: %s\n", reply->str);
		redisFree(*c);
		return REDIS_PING_FAILURE;
	}
	freeReplyObject(reply);
	redisFree(*c);
	return 0;
}

void init_logging() {
	const char *logfile = "/tmp/debug.log";
  	remove(logfile);
	logger_initConsoleLogger(stderr);
	logger_initFileLogger(logfile, 10e6, 5);
	logger_setLevel(LogLevel_DEBUG);
}