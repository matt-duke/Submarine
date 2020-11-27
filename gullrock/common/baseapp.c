#include <stdint.h>
#include <stdio.h>
#include <c-logger/logger.h>
#include <pthread.h>

#include "baseapp.h"

extern const char *__progname;

static void transition(smAppClass_t *app, app_state_t new_state);
static void runState(smAppClass_t *app);

static void do_nothing(smAppClass_t *app) {};
static void do_to_init(smAppClass_t *app);
static void do_to_post(smAppClass_t *app);
static void do_to_running(smAppClass_t *app);
static void do_to_fault(smAppClass_t *app);

app_transition_func_t * app_transition_table[ APP_NUM_STATES ][ APP_NUM_STATES ] = {
    { do_to_init, do_to_post, do_nothing,    do_to_fault },
    { do_nothing, do_nothing, do_to_running, do_to_fault },
    { do_nothing, do_to_post, do_nothing,    do_to_fault },
    { do_nothing, do_to_post, do_nothing,    do_to_fault }
};

app_run_func_t * app_run_table[ APP_NUM_STATES ] = {
    do_nothing, do_nothing, do_nothing, do_nothing
};

int appInit (smAppClass_t *app) {
    app->run = &runState;
    app->transition = &transition;
    app->state = APP_STATE_INIT;
    if (pthread_mutex_init(&app->mutex, PTHREAD_MUTEX_NORMAL) != 0) {
        LOG_FATAL("Mutex init failed.");
    }
    transition(app, app->state);
    return 0;
}

void transition(smAppClass_t *app, app_state_t new_state) {
    app_transition_func_t *transition_fn = 
        app_transition_table[ app->state ][ new_state ];
    pthread_mutex_lock(&app->mutex);
    transition_fn(app);
    if (app->state == new_state) {
        LOG_INFO("Transition to state %d", new_state);
    } else {
        LOG_ERROR("Transition from state %d to state %d failed.", app->state, new_state);
    }
    pthread_mutex_unlock(&app->mutex);
}

void runState(smAppClass_t *app) {
    app_run_func_t *run_fn = app_run_table[ app->state ];

    run_fn(app);
}

void do_to_init(smAppClass_t *app) {
    app->state = APP_STATE_INIT;
}
void do_to_post(smAppClass_t *app) {
    app->state = APP_STATE_POST;
}
void do_to_running(smAppClass_t *app) {
    app->state = APP_STATE_RUNNING;
}
void do_to_fault(smAppClass_t *app) {
    app->state = APP_STATE_FAULT;
}