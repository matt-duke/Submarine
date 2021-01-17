#pragma once

#include <Arduino.h>
#include <Servo_Hardware_PWM.h>

class CameraControl
{
  public:
    // CONSTRUCTOR
    CameraControl::CameraControl(uint8_t YPIN,
                                 uint8_t YMAX,
                                 uint8_t YMIN,
                                 uint8_t PPIN,
                                 uint8_t PMAX,
                                 uint8_t PMIN,
                                 uint16_t SPEED);
    // PUBLIC VARS
    int8_t yaw = 0;   // -100 to 100
    int8_t pitch = 0; // -100 to 100

    // PUBLIC METHODS
    void init();
    int read_yaw();
    int read_pitch();
    bool on_target();
    void update();
    void enable();
    void disable();

  private:
    Servo YawServo;
    Servo PitchServo;
    bool _enabled;
    uint8_t _YPIN;
    uint8_t _YMAX;
    uint8_t _YMIN;
    uint8_t _PPIN;
    uint8_t _PMAX;
    uint8_t _PMIN;
    uint8_t _SPEED;
    bool _EN;
};
