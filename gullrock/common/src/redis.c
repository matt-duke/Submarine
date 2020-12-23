#include <hiredis.h>
#include <async.h>
#include <adapters/libevent.h>
#include <signal.h>
#include <stdlib.h>
#include <stdio.h>
#include <pthread.h>
#include <string.h>
#include <logger.h>
#include <event.h>
#include <event2/thread.h>

#include "redis.h"
#include "common.h"
#include "baseapp.h"

static void *subscriberThread (void *args);

void *subscriberThread(void *args) {
    struct event_base *base = (struct event_base*)args;
    event_base_dispatch(base);
}

int redis_fn_callback (void (*subCallback)(), char *topic, void *privdata) {
    if (0 != evthread_use_pthreads()) {
		LOG_ERROR("Unable to configure libevent for pthreads");
	}
    
    signal(SIGPIPE, SIG_IGN);
    struct event_base *base = event_base_new();
    redisAsyncContext *c = redisAsyncConnect(REDIS_HOSTNAME, REDIS_PORT);
    if (c->err) {
        LOG_ERROR("Error: %s", c->errstr);
    }

    redisLibeventAttach(c, base);
	char cmd[100];
	if (strstr(topic, "*") != NULL) {
		sprintf(cmd, "PSUBSCRIBE %s", topic);
	} else {
		sprintf(cmd, "SUBSCRIBE %s", topic);
	}
	LOG_DEBUG("redis_fn_callback assigned to key: %s", topic);
    redisAsyncCommand(c, subCallback, privdata, cmd);

    pthread_t thread_id;
    int result = pthread_create(&thread_id, NULL, subscriberThread, (void *) base);
    return result;
}

int redis_init_context(redisContext **c) {
	struct timeval timeout = { 1, 500000 };

	*c = redisConnectWithTimeout(REDIS_HOSTNAME, REDIS_PORT, timeout);
	if (*c == NULL || (*c)->err) {
		if (*c) {
			LOG_ERROR("Connection error: %s", (*c)->errstr);
			redisFree(*c);
			return REDIS_CONNECTION_ERROR;
		} else {
			LOG_ERROR("Connection error: can't allocate redis context");
			redisFree(*c);
			return REDIS_ALLOCATION_FAULURE;
		}
	}
	redisReply *reply = redisCommand(*c, "PING");
	if (0 != strcmp(reply->str, "PONG")) {
		LOG_ERROR("Failed to ping Redis server. Replied: %s", reply->str);
		redisFree(*c);
		return REDIS_PING_FAILURE;
	}
	freeReplyObject(reply);
	redisFree(*c);
	return 0;
}

int redis_create_keys() {
	redisContext *c;
	redis_init_context(&c);
	for (int i=0; i<REDIS_NUM_KEYS; i++) {
		char cmd[128];
		sprintf(cmd, "TS.CREATE %s RETENTION %d", 
			REDIS_KEYS[i].name,
			REDIS_KEYS[i].retention
		);
		redisReply *reply = redisCommand(c, "cmd");
		freeReplyObject(reply);
	}
	redisFree(c);
	return 0;
}

int redis_add_sample(redisContext **c, char *key, double value) {
	char cmd[128];
	sprintf(cmd, "TS.ADD %s * %f", key, value);
	
	redisReply *reply = redisCommand(*c, "cmd");
	freeReplyObject(reply);
}