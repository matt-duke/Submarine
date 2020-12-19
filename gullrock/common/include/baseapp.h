#ifndef BASEAPP_H
#define BASEAPP_H

#include <pthread.h>
#include <hiredis.h>

#define RUN_DELAY 2

typedef enum {
    APP_STATE_INIT,
    APP_STATE_POST,
    APP_STATE_RUNNING,
    APP_STATE_FAULT,
    APP_NUM_STATES } app_state_t;

typedef struct smAppClass {
    void (*run)();
    void (*transition)(app_state_t new_state);
    int (*lock)();
    int (*unlock)();
    void (*crash)();
    redisContext *context;
    pthread_mutex_t mutex;
    app_state_t state;
    char *name;
} smAppClass_t;

typedef void app_transition_func_t();
typedef void app_run_func_t();

extern app_transition_func_t * app_transition_table[ APP_NUM_STATES ] [ APP_NUM_STATES ];
extern app_run_func_t * app_run_table[ APP_NUM_STATES ];

int GlobalAppInit();
void *heartbeatThread(void *state);

smAppClass_t GlobalApp;
redisContext *context;

#endif