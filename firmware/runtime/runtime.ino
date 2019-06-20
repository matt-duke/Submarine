#include <EventManager.h>
#include <EEPROM.h>

#define PIN_M1 1
#define PIN_M2 2


EventManager gEM;
EventManager::EventType kSerialMsg;

union SerialBuffer{
  struct
  {
    uint8_t req;
    uint8_t obj;
    int val;
  }data;
  byte whole[4];
};

void processMsg (int eventCode, int eventParam)
{
  Serial.print(eventParam, HEX);
}

void setup()
{
  Serial.begin(115200);
  gEM.addListener( kSerialMsg, processMsg );
}

void loop()
{
  union SerialBuffer test;
  gEM.processEvent();
}

void serialEvent()
{
  Serial.println("serial event");
  if (Serial.available() >= 32) {
    union SerialBuffer msg;
    msg.whole = byte(Serial.read(msg.whole));
    gEM.queueEvent( kSerialMsg, msg.data.val );
  }
}
