#pragma once

#if defined(__AVR_ATmega168__) || defined(__AVR_ATmega328P__) || \
    defined(__AVR_ATmega328PB__) || defined (__AVR_ATmega32U4__)
  #define MC33926Driver_TIMER1_AVAILABLE
#endif

#include <Arduino.h>

#define MAX_SPEED 254
#ifndef M_DELAY
#define M_DELAY 10
#endif

class MC33926Driver
{
  public:
    // CONSTRUCTORS
    // Default pin selection.
    //MC33926Driver();
    // User-defined pin selection.
    MC33926Driver(unsigned char M1IN1,
                           unsigned char M1IN2,
                           unsigned char M1PWM,
                           unsigned char M1FB,
                           unsigned char M1SF,
                           unsigned char M2IN1,
                           unsigned char M2IN2,
                           unsigned char M2PWM,
                           unsigned char M2FB,
                           unsigned char M2SF,
                           unsigned char EN);

    // PUBLIC METHODS
    bool init(); // Initialize TIMER 1, set the PWM to 20kHZ.
    bool setM1Speed(int16_t speed); // Set speed for M1.
    bool setM2Speed(int16_t speed); // Set speed for M2.
    void disable();
    bool enable();
    unsigned int getM1Current(); // Get current reading for M1.
    unsigned int getM2Current(); // Get current reading for M2.
    bool getM1Fault(); // Get fault reading.
    bool getM2Fault();
    bool getFault();
    bool enabled = false;
    int16_t m1Speed = 0;
    int16_t m2Speed = 0;

  private:
    bool _setSpeed(int16_t speed, int16_t *mSpeed, uint8_t PWM, uint8_t IN1, uint8_t IN2);
    unsigned char _M1IN1;
    unsigned char _M1IN2;
    unsigned char _M2IN1;
    unsigned char _M2IN2;
    unsigned char _M1PWM;
    unsigned char _M2PWM;
    unsigned char _M1FB;
    unsigned char _M2FB;
    unsigned char _M1SF;
    unsigned char _M2SF;
    unsigned char _EN;
};
