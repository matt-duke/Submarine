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
#include <assert.h>

#include <redis.h>

#include "mcu.h"

/* Variables */
extern const char *__progname;

#define IO_REGEX "^set\\.io\\.([[:alnum:]_]+)$"

McuClass_t mcu;

/* Functions */

static void do_init();
static void do_post();
static void do_running();
static void do_fault();

static void pubsub(redisAsyncContext *c, void *reply, void *privdata);

int main(int argc, char *argv[]) {
    app_run_table[APP_STATE_INIT] = do_init;
    app_run_table[APP_STATE_POST] = do_post;
    app_run_table[APP_STATE_RUNNING] = do_running;
    app_run_table[APP_STATE_FAULT] = do_fault;

    GlobalAppInit();
    mcuInit(&mcu);

    //temporary
    redis_create_keys(&GlobalApp.context);
    //

    if (0 != redis_fn_callback(&pubsub, "set.io.*", NULL)) {
        LOG_ERROR("Callback init failed.");
    }

    while (1) {
        GlobalApp.run();
        mcu.run(&mcu);
        sleep(0.1);
    }
}

void do_init() {
    GlobalApp.transition(APP_STATE_POST);
    mcu.transition(&mcu, MCU_STATE_POST);
}

void do_post() {
    if (mcu.state == MCU_STATE_POST) {
        return;
    }
    else if (mcu.state == MCU_STATE_READY) {
        GlobalApp.transition(APP_STATE_RUNNING);
    } else if (mcu.state == MCU_STATE_FAULT) {
        GlobalApp.transition(APP_STATE_FAULT);
    }
}

void do_running() {
    if (mcu.state == MCU_STATE_FAULT) {
        GlobalApp.transition(APP_STATE_FAULT);
    }
    for (int i=0;i< REDIS_NUM_KEYS; i++) {
        if (REDIS_KEYS[i].hdlc_key == HDLC_NOT_IMPLEMENTED) {
            break;
        }
        data32_t data;
        mcu.get(&mcu, REDIS_KEYS[i].hdlc_key, &data);
        switch (REDIS_KEYS[i].type) {
            case TYPE_FLOAT:
                push_to_redis(GlobalApp.context, i, &data.f);
                break;
            case TYPE_UINT8:
                push_to_redis(GlobalApp.context, i, &data.ui8[0]);
                break;
            case TYPE_INT8:
                push_to_redis(GlobalApp.context, i, &data.i8[0]);
                break;
            case TYPE_UINT32:
                push_to_redis(GlobalApp.context, i, &data.ui32);
                break;
            case TYPE_INT32:
                push_to_redis(GlobalApp.context, i, &data.i32);
                break;
            default:
                LOG_ERROR("Unexpected type");
                break;
        }
    }

}

void do_fault() {
    if (mcu.state == MCU_STATE_READY) {
        mcu.transition(&mcu, MCU_STATE_READY);
    }
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
    regmatch_t pmatch[2];
    if (regcomp(&regex, IO_REGEX, REG_EXTENDED) != 0) {
        LOG_ERROR("regcomp error");
        return;
    }
    int status = regexec(&regex, msg, 2, pmatch, 0);
    char *key = NULL;
    regfree(&regex);
    if (!status) { 
        key = get_match(msg, &pmatch[1]);
        if (key == NULL) {
            LOG_ERROR("Failed to malloc pointer");
            return;
        }
    } else {
        LOG_WARN("No match found");
        return;
    }
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

    data32_t data;
    switch(REDIS_KEYS[id].type) {
        case TYPE_INT32:
            data.i32 = (int32_t)atoi(r->element[3]->str);
            break;
        case TYPE_UINT32:
            data.ui32 = (uint32_t)atoi(r->element[3]->str);
            break;
        case TYPE_INT16:
            data.i16[0] = (int16_t)atoi(r->element[3]->str);
            break;
        case TYPE_UINT16:
            data.ui16[0] = (uint16_t)atoi(r->element[3]->str);
            break;
        case TYPE_UINT8:
            data.ui8[0] = (uint8_t)atoi(r->element[3]->str);
            break;
        case TYPE_INT8:
            data.i8[0] = (int8_t)atoi(r->element[3]->str);
            break;
        default:
            LOG_ERROR("Invalid hdlc type: %d", REDIS_KEYS[id].type);
            return;
    }
    mcu.set(&mcu, REDIS_KEYS[id].hdlc_key, &data);
}