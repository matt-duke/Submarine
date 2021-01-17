 #include <MemoryFree.h>
#include <Arduino_FreeRTOS.h>
//#include <SparkFun_TB6612.h>

#include "command_handler.h"
#include "def.h"

// Functions
int command_get(packet_t *in_p, packet_t *out_p);
int command_set(packet_t *in_p, packet_t *out_p);

void setup_external() {
    CamCtrl.init();
    MotorDriver.init();

    pinMode(AIN1, OUTPUT);
    pinMode(AIN2, OUTPUT);
    pinMode(PWMA, OUTPUT);
    pinMode(STBY, OUTPUT);
    led_set(0);
}

int command_handler(packet_t *in_p, packet_t *out_p) {
    if (in_p->s.type == HDLC_TYPE_SET) {
        SERIAL_DEBUG.println("SET");
        command_set(in_p, out_p);
    } else if (in_p->s.type == HDLC_TYPE_GET) {
        SERIAL_DEBUG.println("GET");
        command_get(in_p, out_p);
    } else {
        fault_handler();
    }
}

bool test_mode() {
    if (GlobalState == MCU_STATUS_FAULT) {
        return false;
    }
    SERIAL_DEBUG.println("TEST MODE STARTED");
    GlobalState = MCU_STATUS_POST;
    
    SERIAL_DEBUG.println("Motor Test");

    MotorDriver.setM1Speed(254);
    MotorDriver.setM2Speed(254);
    MotorDriver.setM1Speed(0);
    MotorDriver.setM2Speed(0);

    SERIAL_DEBUG.println("Motor Test Done");
    SERIAL_DEBUG.println("LED Test");
    for (int i=0; i<3; i++) {
        for (int ii=0;ii<=255;ii++) {
            led_set(ii);
            delay(2);
        }
        for (int ii=255;ii>=0;ii--) {
            led_set(ii);
            delay(2);
        }
    }
    led_set(0);
    SERIAL_DEBUG.println("LED Test Done");
    SERIAL_DEBUG.println("Servo Test");
    for (int i=0;i<1;i++) {
        CamCtrl.pitch = 0;
        CamCtrl.yaw = 0;
        delay(1);
        while (!CamCtrl.on_target()) {vTaskDelay(1);};
        CamCtrl.pitch = 100;
        CamCtrl.yaw = 100;
        while (!CamCtrl.on_target()) {vTaskDelay(1);};
        CamCtrl.pitch = -100;
        CamCtrl.yaw = 100;
        while (!CamCtrl.on_target()) {vTaskDelay(1);};
        CamCtrl.pitch = -100;
        CamCtrl.yaw = 100;
        while (!CamCtrl.on_target()) {vTaskDelay(1);};
        CamCtrl.pitch = -100;
        CamCtrl.yaw = -100;
        while (!CamCtrl.on_target()) {vTaskDelay(1);};
        CamCtrl.yaw=0;
        CamCtrl.pitch = 0;
        while (!CamCtrl.on_target()) {vTaskDelay(1);};
        delay(1);
    }
    SERIAL_DEBUG.println("Servo Test Done");
    SERIAL_DEBUG.println("TEST MODE ENDED");
    GlobalState = MCU_STATUS_OK;
    return true;
}

int command_get(packet_t *in_p, packet_t *out_p) {
    switch (in_p->s.key) {
        case HDLC_MOTOR_SPEED:
            out_p->s.data32.data16[0].value = MotorDriver.m1Speed;
            out_p->s.data32.data16[1].value = MotorDriver.m2Speed;
            break;
        case HDLC_MOTOR_SF:
            out_p->s.data32.data16[0].value = MotorDriver.getM1Fault();
            out_p->s.data32.data16[1].value = MotorDriver.getM2Fault();
            break;
        case HDLC_MOTOR_CURR:
            out_p->s.data32.data16[0].value = MotorDriver.getM1Current();
            out_p->s.data32.data16[1].value = MotorDriver.getM1Current();
            break;
        case HDLC_STATUS:
            out_p->s.data32.bytes[0] = GlobalState;
            out_p->s.data32.bytes[1] = MotorDriver.getM1Fault();
            out_p->s.data32.bytes[2] = MotorDriver.getM2Fault();
            break;
        case HDLC_FREE_MEM:
            out_p->s.data32.value = freeMemory();
            break;
        case HDLC_CAMERA:
            out_p->s.data32.data16[0].value = CamCtrl.read_yaw();
            out_p->s.data32.data16[1].value = CamCtrl.read_pitch();
            break;
        case HDLC_WATER_TEMP:
            out_p->s.type = HDLC_TYPE_NOT_IMPLEMENTED;
            break;
        case HDLC_TOTAL_CURRENT:
            out_p->s.type = HDLC_TYPE_NOT_IMPLEMENTED;
            break;
        default:
            out_p->s.type = HDLC_TYPE_INVALID;
    }
}

int command_set(packet_t *in_p, packet_t *out_p) {
    switch (in_p->s.key) {
        case HDLC_MOTOR_SPEED:
            bool success = true;
            int16_t speed;
            speed = in_p->s.data32.data16[0].value;
            success &= MotorDriver.setM1Speed(speed);

            speed = in_p->s.data32.data16[1].value;
            success &= MotorDriver.setM2Speed(speed);

            (success) ? out_p->s.type = HDLC_TYPE_SUCCESS: out_p->s.type = HDLC_TYPE_FAILURE;
            break;
        case HDLC_CAMERA:
            CamCtrl.yaw = in_p->s.data32.data16[0].value;
            CamCtrl.pitch = in_p->s.data32.data16[1].value;
            out_p->s.type = HDLC_TYPE_SUCCESS;
            break;
        case HDLC_LED:
            led_set(in_p->s.data32.value);
            out_p->s.type = HDLC_TYPE_SUCCESS;
            break;
        case HDLC_NETWORK_STATUS:
            NetworkStatus.layer1 = in_p->bytes[0];
            NetworkStatus.apc = in_p->bytes[1];
            NetworkStatus.wan = in_p->bytes[2];
            break;
        case HDLC_STATUS:
            switch(in_p->s.data32.value) {
                case MCU_STATUS_OK:

                case MCU_STATUS_POST:
                    xTaskNotifyGive(TaskPOST_handle);
                    break;
                case MCU_STATUS_FAULT:
                    fault_handler();
                    break;
            }
            break;
        default:
            out_p->s.type = HDLC_TYPE_INVALID;
    }
}

void led_set(uint8_t pwm) {
    if (GlobalState != MCU_STATUS_FAULT) {
        if (pwm == 0) {
            // Turns off all pins - for preventing current leakage to +5V (fix in hw later)
            digitalWrite(AIN1, LOW);
            digitalWrite(AIN2, LOW);
            digitalWrite(STBY, LOW);
            analogWrite(PWMA, 0);
        }
        digitalWrite(AIN1, LOW);
        digitalWrite(AIN2, HIGH);
        digitalWrite(STBY, HIGH);
        analogWrite(PWMA, pwm);
    }
}

void fault_handler() {
  SERIAL_DEBUG.println("Entering fault state");
  GlobalState = MCU_STATUS_FAULT;

  digitalWrite(STBY, LOW);
  CamCtrl.disable();
  MotorDriver.disable();
}