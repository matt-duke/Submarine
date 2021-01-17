#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include <logger.h>
#include <pthread.h>
#include <errno.h>
#include <string.h>

#include <hiredis.h>
#include <async.h>
#include <adapters/libevent.h>

#include "baseapp.h"
#include "redis.h"
#include "common.h"

extern const char *__progname;
static pthread_t heartbeat_thread;

static void transition(app_state_t new_state);
static void runState();

static void do_nothing() {};
static void do_to_init();
static void do_to_post();
static void do_to_running();
static void do_to_fault();
static void do_init();

void *heartbeatThread(void *arg);
static void transitionCallback(redisAsyncContext *c, void *reply, void *privdata);
static int lock();
static int unlock();
static void crash();

app_transition_func_t * app_transition_table[ APP_NUM_STATES ][ APP_NUM_STATES ] = {
    { do_to_init, do_to_post, do_nothing,    do_to_fault },
    { do_nothing, do_nothing, do_to_running, do_to_fault },
    { do_nothing, do_to_post, do_nothing,    do_to_fault },
    { do_nothing, do_to_post, do_nothing,    do_to_fault }
};

app_run_func_t * app_run_table[ APP_NUM_STATES ] = {
    do_init, do_nothing, do_nothing, do_nothing
};

int GlobalAppInit() {
    init_logging();
    redis_init_keys();

    GlobalApp.run = &runState;
    GlobalApp.name = (char *)__progname;
    GlobalApp.transition = &transition;
    GlobalApp.state = APP_STATE_INIT;
    GlobalApp.context = context;
    GlobalApp.crash = &crash;

    pthread_mutexattr_t attr;
    pthread_mutexattr_init(&attr);
    pthread_mutexattr_settype(&attr, PTHREAD_MUTEX_RECURSIVE);
    if (pthread_mutex_init(&GlobalApp.mutex, &attr) != 0) {
        LOG_FATAL("Mutex init failed.");
        exit(1);
    }
    pthread_mutexattr_destroy(&attr);
	pthread_create(&heartbeat_thread, NULL, heartbeatThread, NULL);

    char key[strlen(__progname)+11];
    char transition_key = sprintf(key, "%s.transition", __progname);
    if (0 != redis_fn_callback(&transitionCallback, key, NULL)) {
        LOG_ERROR("Callback init failed.");
    }
    if (redis_init_context(&GlobalApp.context) != 0) {
        LOG_FATAL("Failed to start.");
    }
    GlobalApp.transition(GlobalApp.state);
    return 0;
}

void transition(app_state_t new_state) {
    app_transition_func_t *transition_fn = 
        app_transition_table[ GlobalApp.state ][ new_state ];
    LOG_INFO("%s transition requested from: %d to %d", __progname, GlobalApp.state, new_state);
    if (0 == lock()) {
        transition_fn();
        if (GlobalApp.state == new_state) {
            LOG_INFO("Successful transition to state %d", new_state);
        } else {
            LOG_ERROR("Transition from state %d to state %d failed.", GlobalApp.state, new_state);
            if (new_state == APP_STATE_FAULT) {
                LOG_FATAL("Failed to transition to fault state.");
                crash();
            }
        }
        unlock();
    } else {
        LOG_ERROR("Failed to lock");
    }
}

void runState() {
    app_run_func_t *run_fn = app_run_table[ GlobalApp.state ];

    if (0 == lock()) {
        run_fn();
        unlock();
    } else {
        LOG_ERROR("Failed to lock.");
    }
}

void do_to_init() {
    GlobalApp.state = APP_STATE_INIT;
}
void do_to_post() {
    GlobalApp.state = APP_STATE_POST;
}
void do_to_running() {
    GlobalApp.state = APP_STATE_RUNNING;
}
void do_to_fault() {
    GlobalApp.state = APP_STATE_FAULT;
}

void do_init() {
    GlobalApp.transition(APP_STATE_POST);
}

void transitionCallback(redisAsyncContext *c, void *reply, void *privdata) {
    LOG_DEBUG("transition callback");
    redisReply *r = reply;
    //freeReplyObject(r);
}

int lock() {
    //LOG_DEBUG("Locking %s", __progname);
    int ret = pthread_mutex_lock(&GlobalApp.mutex);
    if (ret == 0) {
        //LOG_DEBUG("Lock aquired %s", __progname);
    } else {
        if (ret == EINVAL) {
            LOG_ERROR("Mutex not initialized %s", __progname);
        } else if (ret == EDEADLK) {
            LOG_ERROR("Mutex in deadlock %s", __progname);
        } else if (ret == EAGAIN) {
            LOG_ERROR("Max recursive locks %s", __progname);
        } else if (ret == EBUSY) {
            LOG_ERROR("Lock already acquired %s", __progname);
        } else {
            LOG_ERROR("Unknown lock error %s", __progname);
        }
        exit(ret);
    }
    return(ret);
}

int unlock() {
    //LOG_DEBUG("Unlocking %s", __progname);
    int ret = pthread_mutex_unlock(&GlobalApp.mutex);
    if (ret == 0) {
        //LOG_DEBUG("Lock released %s", __progname);
    } else {
        if (ret == EINVAL) {
            LOG_ERROR("Mutex not initialized %s", __progname);
        } else if (ret == EPERM) {
            LOG_ERROR("Failed to unlock. Current thread does not own mutex %s", __progname);
        } else if (ret == EAGAIN) {
            LOG_ERROR("Max recursive locks %s", __progname);
        } else {
            LOG_ERROR("Unknown unlock error %s", __progname);
        }
        exit(ret);
    }
    return(ret);
}

void crash() {
    pthread_cancel(heartbeat_thread);
    exit(1);
}

void *heartbeatThread(void *arg) {
    init_logging();

	LOG_INFO("Starting heartbeat: %s", __progname);

    redisContext *c;
  	struct timeval timeout = { 1, 500000 };

	c = redisConnectWithTimeout(REDIS_HOSTNAME, REDIS_PORT, timeout);
	if (c == NULL || c->err) {
		if (c) {
            LOG_ERROR("Connection error: %s", c->errstr);
            redisFree(c);
            abort();
		} else {
            LOG_ERROR("Connection error: can't allocate redis context");
            redisFree(c);
            crash();
		}
	}

	while (1) {
        if (0 == lock()) {
            redisReply *h_reply;
            LOG_DEBUG("heartbeat %d", GlobalApp.state);
            h_reply = redisCommand(c, "SET %s %d EX %d", __progname, GlobalApp.state, TIMEOUT_HEARTBEAT);
            if (0 != strcmp(h_reply->str, "OK")) {
                LOG_ERROR("Failure setting value: %s", h_reply->str);
            }
            freeReplyObject(h_reply);
            unlock();
        } else {
            LOG_ERROR("Failed to lock");
        }
        sleep(HEARTBEAT_RATE);
	}
    redisFree(c);
}