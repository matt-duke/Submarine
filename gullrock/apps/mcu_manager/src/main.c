#include <async.h>
#include <baseapp.h>
#include <common.h>
#include <hiredis.h>
#include <logger.h>
#include <pthread.h>
#include <redis.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include "mcu.h"

/* Variables */
extern const char *__progname;

#define IO_REGEX "^(set|get)\\.io\\.([[:alnum:]_]+)$"

McuClass_t mcu;

/* Functions */

static void do_init();
static void do_post();
static void do_running();
static void do_fault();

static void pubsub(redisAsyncContext *c, void *reply, void *privdata);
static void mcu_to_redis(int key_index);
static void redis_to_mcu(int key_index);

int main(int argc, char *argv[]) {
    app_run_table[APP_STATE_INIT] = do_init;
    app_run_table[APP_STATE_POST] = do_post;
    app_run_table[APP_STATE_RUNNING] = do_running;
    app_run_table[APP_STATE_FAULT] = do_fault;

    GlobalAppInit();
    mcuInit(&mcu);

    if (0 != redis_fn_callback(&pubsub, "[sg]et.io.*", NULL)) {
        LOG_ERROR("Callback init failed.");
    }

    while (1) {
        GlobalApp.run();
        mcu.run(&mcu);
        sleep(2);
    }
}

void do_init() {
    GlobalApp.transition(APP_STATE_POST);
    mcu.transition(&mcu, MCU_STATE_POST);

    //temporary
    redis_create_keys(&GlobalApp.context);
    //
}

void do_post() {
    bool criteria = true;
    if (mcu.state != MCU_STATE_POST) {
        criteria = false;
    }
    time_t start = time(NULL);
    while (mcu.state == MCU_STATE_POST) {
        if (time(NULL) - start > 30) {
            criteria = false;
            LOG_ERROR("POST failed.");
            break;
        }
    }
    if (!criteria) {
        GlobalApp.transition(APP_STATE_FAULT);
    } else {
        GlobalApp.transition(APP_STATE_RUNNING);
    }
}

void do_running() {
    if (mcu.state == MCU_STATE_FAULT) {
        GlobalApp.transition(APP_STATE_FAULT);
    }
}

void do_fault() {
    if (mcu.state != MCU_STATE_FAULT) {
        mcu.transition(&mcu, MCU_STATE_POST);
    }
}

void mcu_to_redis(int key_index ) {
    redisReply *reply = redisCommand(GlobalApp.context, "");
    
}

void redis_to_mcu(int key_index) {
    
}

void pubsub(redisAsyncContext *c, void *reply, void *privdata) {
    redisReply *r = reply;
    if (reply == NULL) {
        LOG_DEBUG("Reply is NULL");
        return;
    }
    if (r->type != REDIS_REPLY_ARRAY) {
        LOG_DEBUG("Reply is not an array");
        return;
    }
    if (r->element[2]->type != REDIS_REPLY_STRING) {
        LOG_DEBUG("Reply is not an string");
        return;
    }
    char *msg = r->element[2]->str;
    if (msg == NULL) {
        LOG_DEBUG("msg is NULL");
        return;
    }
    regex_t regex;
    regmatch_t pmatch[3];
    if (regcomp(&regex, IO_REGEX, REG_EXTENDED) != 0) {
        LOG_ERROR("regcomp error");
        return;
    }
    int status = regexec(&regex, msg, 3, pmatch, 0);
    char *key = NULL;
    char *type = NULL;
    regfree(&regex);
    if (!status) { 
        type = get_match(msg, &pmatch[1]); 
        key = get_match(msg, &pmatch[2]);
        if (key == NULL || type == NULL) {
            LOG_ERROR("Failed to malloc pointer");
            return;
        }
    } else {
        LOG_WARN("No match found");
        return;
    }
    int data = (int)atoi(r->element[3]->str);
    int id = -1;
    for (int i = 0; i < REDIS_NUM_KEYS; i++) {
        if (REDIS_KEYS[i].key == NULL) {
            break;
        }
        if (0 == strcmp(REDIS_KEYS[i].key, key)) {
            if (REDIS_KEYS[i].hdlc_key == HDLC_NOT_IMPLEMENTED) {
                LOG_WARN("Ignoring key %s: hdlc_key=%d", key, REDIS_KEYS[i].hdlc_key);
                break;
            }
            id = i;
            break;
        }
    }
    if (id == -1) {
        LOG_ERROR("Invalid key %s", key);
        return;
    }
    free(key);
    if (0 == strcmp("test", "get")) {

    } else if (0 == strcmp("test", "set")) {

    }
    free(type);
}