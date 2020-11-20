#ifndef MOTOR_H
#define MOTOR_H

typedef enum { 
    MOTOR_STATE_IDLE,
    MOTOR_STATE_STOPPED,
    MOTOR_STATE_CHANGE_SPEED,
    MOTOR_NUM_STATES } motor_state_t;

typedef struct sMotorClass {
    void (*run)(struct sMotorClass *self);
    void (*transition)(struct sMotorClass *self, motor_state_t new_state);
    motor_state_t state;
    int speed;
} MotorClass_t;

int motorInit (MotorClass_t *motor);

#endif