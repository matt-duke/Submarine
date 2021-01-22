#include "MC33926Driver.h"

// Constructors ////////////////////////////////////////////////////////////////

/*MC33926Driver::MC33926Driver()
{
  //Pin map
  _nD2 = 4;
  _M1DIR = 7;
  _M1PWM = 9;
  _M2DIR = 8;
  _M2PWM = 10;
  _nSF = 12;
  _M1FB = A0;
  _M2FB = A1;
}
*/
MC33926Driver::MC33926Driver(unsigned char M1IN1,
                                               unsigned char M1IN2,
                                               unsigned char M1PWM,
                                               unsigned char M1FB,
                                               unsigned char M1SF,
                                               unsigned char M2IN1,
                                               unsigned char M2IN2,
                                               unsigned char M2PWM,
                                               unsigned char M2FB,
                                               unsigned char M2SF,
                                               unsigned char EN)
{
  _M1IN1 = M1IN1;
  _M1IN2 = M1IN2;
  _M1PWM = M1PWM;
  _M2IN1 = M2IN2;
  _M2IN2 = M2IN2;
  _M2PWM = M2PWM;
  _M1FB = M1FB;
  _M2FB = M2FB;
  _M1SF= M1SF;
  _M2SF= M2SF;
  _EN= EN;
}

// Public Methods //////////////////////////////////////////////////////////////
bool MC33926Driver::init()
{
  pinMode(_M1IN1,OUTPUT);
  pinMode(_M1IN2,OUTPUT);
  pinMode(_M1PWM,OUTPUT);
  pinMode(_M1FB,INPUT);
  pinMode(_M2IN1,OUTPUT);
  pinMode(_M2IN2,OUTPUT);
  pinMode(_M2PWM,OUTPUT);
  pinMode(_M2FB,INPUT);
  pinMode(_M1SF,INPUT);
  pinMode(_M2SF,INPUT);
  pinMode(_EN,OUTPUT);

  return enable();
}

bool MC33926Driver::_setSpeed(int16_t speed, int16_t *mSpeed, uint8_t PWM, uint8_t IN1, uint8_t IN2) {
  if (!MC33926Driver::enabled) {
    return false;
  }

  if (speed > 255) {
    speed = 255;
  } else if (speed < -255) {
    speed = -255;
  }

  if ((speed<0) != (*mSpeed<0)) {
    // Switch direction, stop motor
    analogWrite(PWM, 255);
    if (speed > 0) {
      digitalWrite(IN1,HIGH);
      digitalWrite(IN2,LOW);
    } else {
      digitalWrite(IN1,LOW);
      digitalWrite(IN2,HIGH);
    }
  }

  int8_t add = 0;
  if (speed > *mSpeed) {
    add = 1;
  } else if (speed < *mSpeed) {
    add = -1;
  }

  for (int16_t i=*mSpeed;i!=speed;i+=add) {
    analogWrite(PWM, abs(~i)); // map 400 to 255
    delay(M_DELAY);
  }

  *mSpeed = speed;
  return true;
}

// Set speed for motor 1
bool MC33926Driver::setM1Speed(int16_t speed)
{
  return MC33926Driver::_setSpeed(speed, &(MC33926Driver::m1Speed), _M1PWM, _M1IN1, _M1IN2);
}

// Set speed for motor 2
bool MC33926Driver::setM2Speed(int16_t speed)
{
  return MC33926Driver::_setSpeed(speed, &(MC33926Driver::m2Speed), _M2PWM, _M2IN1, _M2IN2);
}

// Return motor 1 current value in milliamps.
unsigned int MC33926Driver::getM1Current()
{
  // 5V / 1024 ADC counts / 525 mV per A = 9 mA per count
  return analogRead(_M1FB) * 9;
}

// Return motor 2 current value in milliamps.
unsigned int MC33926Driver::getM2Current()
{
  // 5V / 1024 ADC counts / 525 mV per A = 9 mA per count
  return analogRead(_M2FB) * 9;
}

// Return M2 error status
bool MC33926Driver::getM1Fault()
{
  if (digitalRead(_M1PWM) == 1) {
    return false;
  } else {
    bool SF = !digitalRead(_M1SF);
    if (SF) {
      disable();
    }
    return SF;
  }
}

// Return M1 error status
bool MC33926Driver::getM2Fault()
{
  if (digitalRead(_M2PWM) == 1) {
    return false;
  } else {
    bool SF = !digitalRead(_M2SF);
    if (SF) {
      disable();
    }
    return SF;
  }
}

// Return combined error status
bool MC33926Driver::getFault()
{
  return getM1Fault() && getM2Fault();
}

void MC33926Driver::disable() {
  enabled = false;
  digitalWrite(_EN, LOW);
  digitalWrite(_M1IN1,LOW);
  digitalWrite(_M1IN2,LOW);
  digitalWrite(_M2IN1,LOW);
  digitalWrite(_M2IN2,LOW);
}

bool MC33926Driver::enable() {
  if (getFault()) {    
    disable();
    return 1;
  } else {
    enabled = true;
    digitalWrite(_M1IN1,HIGH);
    digitalWrite(_M1IN2,LOW);
    digitalWrite(_M2IN1,HIGH);
    digitalWrite(_M2IN2,LOW);
    digitalWrite(_EN, HIGH);
    return 0;
  }
}