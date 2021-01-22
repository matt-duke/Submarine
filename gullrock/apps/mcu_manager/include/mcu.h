#ifndef MCU_H
#define MCU_H

#include <hdlc_def.h>

typedef struct sMcuClass {
    void (*run)(struct sMcuClass *self);
    int (*transition)(struct sMcuClass *self, mcu_state_t new_state);
    int (*get)(struct  sMcuClass *self, uint8_t key, data32_t *data);
    int (*set)(struct sMcuClass *self, uint8_t key, data32_t *data);
    void (*flush)();
    void (*reset)();
    mcu_state_t state;
} McuClass_t;

extern void mcuInit (McuClass_t *mcu);

#endif