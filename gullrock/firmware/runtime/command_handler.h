#pragma once

#include <Arduino.h>
#include <hdlc_def.h>

#include "def.h"

void command_handler(packet_t *in_p, packet_t *out_p);
bool test_mode();
void led_set(uint8_t pwm);
void setup_external();
void fault_handler();
