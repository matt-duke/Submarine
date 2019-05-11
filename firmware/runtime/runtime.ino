#include <EventManager.h>
#include <EEPROM.h>

struct pins {
    byte M1 = 1;
    byte M2 = 2;
    byte L1 = 3;
}

struct data {
    string name;
    float val = 0;
}

enum states {
    init,
    test,
    normal,
    critical
}

union addrByte32{
    uint32_t val;
    uint8_t data[4];
}

addrByte32 CRC;
const pin Pins;
currState states = init
EventManager eventMgr;
data dataTbl[];

bool addData(string name) {
    dataTbl[sizeof(dataTbl)+1].name=name;
}

bool test() {
    bool result = True
    return result;
}

void setup()
{   
    pinMode(pin.M1, OUTPUT);
    pinMode(pin.M2, OUTPUT);
    pinMode(pin.L2, OUTPUT);
    
    addData("current")
    
    for (i=0;i<sizeof(CRC.array);i++;) {
        crc.array[i] = EEPROM.read(i)
    }
    currState = test;
}

void loop()
{
    if (currState == test) {
        result=test()
        if (!result) {
            currState = critical;
        }
        else {
            currState = normal;
        }
    }
}
