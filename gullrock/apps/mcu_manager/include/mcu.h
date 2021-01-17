#ifndef MCU_H
#define MCU_H

#include <hdlc_def.h>

typedef enum { 
    MCU_STATE_INIT,
    MCU_STATE_POST,
    MCU_STATE_READY,
    MCU_STATE_FAULT,
    MCU_NUM_STATES } mcu_state_t;

typedef struct sMcuClass {
    void (*run)(struct sMcuClass *self);
    int (*transition)(struct sMcuClass *self, mcu_state_t new_state);
    int (*get)(struct  sMcuClass *self, uint8_t key, data32_t *data);
    int (*set)(struct sMcuClass *self, uint8_t key);
    mcu_state_t state;
} McuClass_t;

extern int mcuInit (McuClass_t *mcu);

#endif