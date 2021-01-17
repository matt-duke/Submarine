#include "CameraControl.h"

#define IMIN -100
#define IMAX 100

// Constructors ////////////////////////////////////////////////////////////////

CameraControl::CameraControl(uint8_t YPIN,
                             uint8_t YMAX,
                             uint8_t YMIN,
                             uint8_t PPIN,
                             uint8_t PMAX,
                             uint8_t PMIN,
                             uint16_t SPEED)
{
  _YPIN = YPIN;
  _YMAX = YMAX;
  _YMIN = YMIN;
  _PPIN = PPIN;
  _PMAX = PMAX;
  _PMIN = PMIN;
  _SPEED = SPEED;
}

void CameraControl::init() {
  YawServo.attach(_YPIN);
  PitchServo.attach(_PPIN);
  enable();
}

bool CameraControl::on_target() {
  int yacc = abs(IMAX-IMIN)/abs(_YMAX-_YMIN);
  int ydiff = abs(read_yaw()-yaw);
  int pacc = abs(IMAX-IMIN)/abs(_PMAX-_PMIN);
  int pdiff = abs(read_pitch()-pitch);
  bool result = ydiff <= yacc;
  result = result && (pdiff <= pacc);
  return result;
}

int CameraControl::read_yaw() {
  return map(YawServo.read(), _YMIN, _YMAX, IMIN, IMAX);
}

int CameraControl::read_pitch() {
  return map(PitchServo.read(), _PMIN, _PMAX, IMIN, IMAX);
}

void CameraControl::update() {
  if (_EN) {
    if (yaw < IMIN) {
      yaw = IMIN;
    }
    if (yaw > IMAX) {
      yaw = IMAX;
    }

    if (pitch < IMIN) {
      pitch = IMIN;
    }
    if (pitch > IMAX) {
      pitch = IMAX;
    }

    uint8_t ypwm = map(yaw, IMIN, IMAX, _YMIN, _YMAX);
    int ynow = YawServo.read();
    if (ypwm > ynow) {
      YawServo.write(ynow + 1);
    } else if (ypwm < ynow) {
      YawServo.write(ynow - 1);
    }

    uint8_t ppwm = map(pitch, IMIN, IMAX, _PMIN, _PMAX);
    int pnow = PitchServo.read();
    if (ppwm > pnow) {
      PitchServo.write(pnow + 1);
    } else if (ppwm < pnow) {
      PitchServo.write(pnow - 1);
    }
  delay(_SPEED);
  }
}

void CameraControl::enable() {
  _EN = true;

}

void CameraControl::disable() {
  _EN = false;
}