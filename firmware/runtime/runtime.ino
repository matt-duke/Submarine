#include <EventManager.h>
#include <EEPROM.h>


union CRC {
    byte length = 4
    byte array[length];
    uint32_t dec;
}
crc CRC;

void setup()
{
    for (i=0;i<crc.length;i++;) {
        crc.array[i] = EEPROM.read(i)
    }
}

void loop()
{
}
