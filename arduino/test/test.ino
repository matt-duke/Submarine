#include <Wire.h>
#define SLAVE_ADDRESS 0x04

int number = 0;
int mode = 0;
int read;

void receiveData(int byteCount) {
  while (Wire.available()) {
    read = Wire.read();
    Serial.println(read);
  }
}
void sendData() {
  byte var[3] = {1,2,3};
  Wire.write(3);
  //Wire.write(var,3);
}

void setup() {
  Serial.begin(9600);
  Wire.begin(SLAVE_ADDRESS);
  Wire.onReceive(receiveData);
  Wire.onRequest(sendData);
}

void loop() {
  Serial.println("Running");
  delay(1000);
}