#include <EEPROM.h>

#define motorLPin  10
#define motorRPin 11
#define compPin 12
#define lightPin 13

#define Ain 4
#define a0 5
#define a1 6
#define a2 7

int motorCal[3];
const char modeTypes[3] = {'INIT','NORMAL','EMERG'};
char mode = modeTypes[2];

void setup() {
  pinMode(motorLPin, OUTPUT);
  pinMode(motorRPin, OUTPUT);
  pinMode(compPin, OUTPUT);
  pinMode(lightPin, OUTPUT);
  pinMode(Ain, INPUT);
  pinMode(a0, OUTPUT);
  pinMode(a1, OUTPUT);
  pinMode(a2, OUTPUT);

  //load calibration values
  for(int i=0;i++;i<3){ motorCal[i] = EEPROM.read(i);}
}

void loop() {
  
}

bool setMotor(char type, int speed) {
  int motor;
  bool returnVar;
  if (type == 'L') {motor = motorLPin;}
  else if (type == 'R') {motor = motorRPin;}
  else if (type == 'C') {motor = compPin;}
  else {returnVar = false;}
  //write speed to motor, including calibration
  return returnVar;
}

int readSensor (int port, int sampleSize)
{
  int r0 = bitRead(port, 0);
  int r1 = bitRead(port, 1);
  int r2 = bitRead(port, 2);
  digitalWrite(a0, r0);
  digitalWrite(a1, r1);
  digitalWrite(a2,r2);
  int value = 0;
  for (int i=0;i++;i<sampleSize) { value += analogRead(A1); }
  value = value / sampleSize;
  return value;
}

void calibrateMotor() {
  //Calibration procedure
  motorCal[0] = 0;
  motorCal[1] = 0;
  EEPROM.update(0, motorR);
  EEPROM.update(1, motorL);
}

void calibrateComp() {
  //compressor calibration
  motorCal[3] = 0;
  EEPROM.update(3, compr);
}

void writeRPI() {
  
}

void readRPI() {
  
}

