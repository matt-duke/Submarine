#include <Wire.h>
#define SLAVE_ADDRESS 0x04
#define LED  13
int number = 0;
int mode = 0;
int read;

void receiveData(int byteCount) {
  while (Wire.available()) {
    read = Wire.read();
  }
}
void sendData() {
  byte var[3] = {1,2,3};
  Wire.write(var,3);
}

void setup() {
  Wire.begin(SLAVE_ADDRESS);
  Wire.onReceive(receiveData);
  Wire.onRequest(sendData);
}

void loop() {
  delay(100);
  if(read == 10) {
    mode = 1;
  } else {
    mode = 0;
  }
}