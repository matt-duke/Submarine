#include "Sensors.h"

// Constructors ////////////////////////////////////////////////////////////////

Sensor::Sensor(float (*f)(), uint8_t wait) {
  _read = *f;
  _wait = wait;
}

/*Sensor::Sensor(uint8_t pin, uint16_t wait, float modifier, const uint16_t buffer_size)
{
  _pin = pin;
  _wait = wait;
  _modifier = modifier;
  delete _buffer;
  CircularBuffer<float,buffer_size> _buffer;
}*/

// Public Methods //////////////////////////////////////////////////////////////
float Sensor::read() {
  for (int i=0;i<_buffer.capacity;i++) {
    float sample = (float)Sensor::_read();
    _buffer.push(sample);
  }
  float avg = 0;
  for (int i=0;i<_buffer.capacity;i++) {
    avg += _buffer[i];
  }
  avg = avg / _buffer.capacity;
  Sensor::value = avg;
  return Sensor::value;
}