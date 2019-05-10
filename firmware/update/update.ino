#include <EEPROM.h>

#define DEBUG 0

void printBin(byte myByte){
 for(byte mask = 0x80; mask; mask >>= 1){
   if(mask & myByte)
       Serial.print('1');
   else
       Serial.print('0');
 }
  Serial.println();
}

union crc {
  uint32_t val;
  uint8_t bytes[4];
};
union crc CRC;

void setup()
{
  Serial.begin(115200);
  int8_t i=sizeof(CRC.bytes)-1;
  while (i>=0) {
    if (Serial.available() > 0) {
      CRC.bytes[i]=Serial.read();
      if (DEBUG) {
        printBin(CRC.bytes[i]);
        Serial.println(i);
      }
      i--;
    }
  }

  if (DEBUG) {
    Serial.println("Byte array:");
    for (byte i=0;i<sizeof(CRC.bytes);i++) {
      Serial.print(i);
      Serial.print(": ");
      Serial.print(CRC.bytes[i]);
      Serial.println();
    }
  }
  
  for (byte i=0;i<sizeof(CRC.bytes);i++) {
    if(EEPROM.read(i) != CRC.bytes[i]){
      EEPROM.write(i, CRC.bytes[i]);
    }
  }
  bool check = 1;
  for (byte i=0;i<sizeof(CRC.bytes);i++) {
    check &=(CRC.bytes[i] == EEPROM.read(i));
  }
  Serial.println(check);
  Serial.println(CRC.val, DEC);
}

void loop() {}
