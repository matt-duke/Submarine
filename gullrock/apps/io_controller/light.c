#include <stdint.h>
#include <stdio.h>
#include <logger/logger.h>

#include "motor.h"


typedef void transition_func_t(MotorClass_t *motor);
typedef void run_func_t(MotorClass_t *motor);

void motorTransition(MotorClass_t *motor, motor_state_t new_state);
void motorRunState(MotorClass_t *motor);

void do_nothing();
void do_idle_to_stopped();
void do_idle_to_change_speed();
void do_stopped_to_idle();

transition_func_t * const transition_table[ MOTOR_NUM_STATES ][ MOTOR_NUM_STATES ] = {
    { do_nothing,         do_idle_to_stopped, do_idle_to_change_speed },
    { do_stopped_to_idle, do_nothing,         do_nothing },
    { do_nothing,         do_nothing,         do_nothing }
};

run_func_t * const run_table[ MOTOR_NUM_STATES ] = {
    do_nothing, do_nothing, do_nothing
};

void do_nothing(MotorClass_t *motor) {

}

void do_idle_to_stopped(MotorClass_t *motor) {
    
}

void do_idle_to_change_speed(MotorClass_t *motor) {
    
}

void do_stopped_to_idle(MotorClass_t *motor) {
    //check entry conditions
    LOG_INFO("entering idle");
    motor->curr_state = MOTOR_STATE_IDLE;
}

int motorInit (MotorClass_t *motor) {
    motor->run = &motorRunState;
    motor->transition = &motorTransition;
    motor->curr_state = MOTOR_STATE_STOPPED;
    return 0;
}

void motorTransition(MotorClass_t *motor, motor_state_t new_state) {
    transition_func_t *transition_fn = 
        transition_table[ motor->curr_state ][ new_state ];

    transition_fn(motor);
}

void motorRunState(MotorClass_t *motor) {
    run_func_t *run_fn = run_table[ motor->curr_state ];

    run_fn(motor);
}