#pragma once

#include <Arduino.h>
#include <CircularBuffer.h>

#ifndef BUFFER_SIZE
#define BUFFER_SIZE 10
#endif

class Sensor
{
  public:
    // CONSTRUCTORS
    //AnalogSensor(uint8_t pin, uint16_t wait, float modifier);
    Sensor(float (*f)(), uint8_t wait);
    // PUBLIC METHODS
    float read();
    float value;

  private:
    float (*_read)();
    uint8_t _wait;
    CircularBuffer<float,BUFFER_SIZE> _buffer;
};
