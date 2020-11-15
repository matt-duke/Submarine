#ifndef MCU_H
#define MCU_H

typedef enum { 
    MCU_STATE_INIT,
    MCU_STATE_POST,
    MCU_STATE_READY,
    MCU_STATE_FAULT,
    MCU_NUM_STATES } mcu_state_t;

typedef struct sMcuClass {
    void (*run)(struct sMcuClass *self);
    int (*transition)(struct sMcuClass *self, mcu_state_t new_state);
    int (*get)(struct sMcuClass *self, int key, int data);
    int (*set)(struct sMcuClass *self, int key, int data);
    mcu_state_t state;
} McuClass_t;

int mcuInit (McuClass_t *Mcu);

#endif