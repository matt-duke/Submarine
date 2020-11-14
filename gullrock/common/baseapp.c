#include <stdint.h>
#include <stdio.h>
#include <logger/logger.h>
#include <pthread.h>

#include "baseapp.h"

extern const char *__progname;

void transition(smAppClass_t *app, app_state_t new_state);
void runState(smAppClass_t *app);
void do_nothing(smAppClass_t *app) {};

app_transition_func_t * app_transition_table[ APP_NUM_STATES ][ APP_NUM_STATES ] = {
    { do_nothing, do_nothing, do_nothing },
    { do_nothing, do_nothing, do_nothing },
    { do_nothing, do_nothing, do_nothing }
};

app_run_func_t * app_run_table[ APP_NUM_STATES ] = {
    do_nothing, do_nothing, do_nothing
};

int appInit (smAppClass_t *app) {
    app->run = &runState;
    app->transition = &transition;
    app->curr_state = APP_STATE_INIT;
    if (pthread_mutex_init(&app->mutex, PTHREAD_MUTEX_NORMAL) != 0) {
        LOG_FATAL("Mutex init failed.");
    }
    transition(app, app->curr_state);
    return 0;
}

void transition(smAppClass_t *app, app_state_t new_state) {
    app_transition_func_t *transition_fn = 
        app_transition_table[ app->curr_state ][ new_state ];
    pthread_mutex_lock(&app->mutex);
    transition_fn(app);
    pthread_mutex_unlock(&app->mutex);
}

void runState(smAppClass_t *app) {
    app_run_func_t *run_fn = app_run_table[ app->curr_state ];

    run_fn(app);
}