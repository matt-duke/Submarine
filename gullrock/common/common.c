#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <signal.h>
#include <pthread.h>

#include <c-logger/logger.h>
#include <hiredis-vip/hiredis.h>
#include <hiredis-vip/async.h>
#include <hiredis-vip/adapters/libevent.h>

#include "redis_def.h"
#include "baseapp.h"
#include "common.h"

/* Variables */
extern const char *__progname;

/* Functions */
int redis_fn_callback (void (*f)(), char *topic);
int init_redis(redisContext **c, const char *hostname, const int port);
void *heartbeatThread(void *state);
void init_logging();


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

void *heartbeatThread(void *state) {
	smAppClass_t *sm = (smAppClass_t*)state;

	LOG_INFO("Starting heartbeat: %s\n", __progname);
  	redisContext *c;
  	init_redis(&c, REDIS_HOSTNAME, REDIS_PORT);

	while (1) {
    	redisReply *h_reply;
		pthread_mutex_lock(&sm->mutex);
		h_reply = redisCommand(c, "SET %s %d EX %d", __progname, sm->state, TIMEOUT_HEARTBEAT);
		pthread_mutex_unlock(&sm->mutex);
		freeReplyObject(h_reply);
    if (!strcmp(h_reply->str, "OK")) {
      LOG_ERROR("Failure setting value: %s\n", h_reply->str);
    }
		sleep(HEARTBEAT_RATE);
	}
}

void init_logging() {
	const char *logfile = "/tmp/debug.log";
  	remove(logfile);
	logger_initConsoleLogger(stderr);
	logger_initFileLogger(logfile, 10e6, 5);
	logger_setLevel(LogLevel_DEBUG);
}