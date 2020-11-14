#ifndef BASEAPP_H
#define BASEAPP_H

#include <pthread.h>

typedef enum {
    APP_STATE_INIT,
    APP_STATE_RUNNING,
    APP_STATE_FAULT,
    APP_NUM_STATES } app_state_t;

typedef struct smAppClass {
    void (*run)(struct smAppClass *self);
    void (*transition)(struct smAppClass *self, app_state_t new_state);
    void (*run_table)(struct smAppClass *self);
    pthread_mutex_t mutex;
    app_state_t curr_state;
} smAppClass_t;

typedef void app_transition_func_t(smAppClass_t *app);
typedef void app_run_func_t(smAppClass_t *app);

extern app_transition_func_t * app_transition_table[ APP_NUM_STATES ] [ APP_NUM_STATES ];
extern app_run_func_t * app_run_table[ APP_NUM_STATES ];

int appInit (smAppClass_t *app);

#endif