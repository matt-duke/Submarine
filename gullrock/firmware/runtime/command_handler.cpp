 #include <MemoryFree.h>
#include <Arduino_FreeRTOS.h>
//#include <SparkFun_TB6612.h>

#include "crc.h"
#include "command_handler.h"
#include "def.h"

// Functions
void command_get(packet_t *in_p, packet_t *out_p);
void command_set(packet_t *in_p, packet_t *out_p);

void setup_external() {
    //CamCtrl.init();
    //MotorDriver.init();

    pinMode(AIN1, OUTPUT);
    pinMode(AIN2, OUTPUT);
    pinMode(PWMA, OUTPUT);
    pinMode(STBY, OUTPUT);
    led_set(0);
}

void command_handler(packet_t *in_p, packet_t *out_p) {
    if (in_p->s.type == HDLC_TYPE_SET) {
        command_set(in_p, out_p);
    } else if (in_p->s.type == HDLC_TYPE_GET) {
        command_get(in_p, out_p);
    } else {
        out_p->s.type = (uint8_t)HDLC_TYPE_NOT_IMPLEMENTED;
    }
}

void command_get(packet_t *in_p, packet_t *out_p) {
    SERIAL_DEBUG.print("GET: ");
    SERIAL_DEBUG.println(in_p->s.key);

    out_p->s.type = (uint8_t)HDLC_TYPE_SUCCESS;
    switch (in_p->s.key) {
        case HDLC_M1_SPEED:
            SERIAL_DEBUG.println("HDLC_M1_SPEED");
            out_p->s.d32.ui8[0] = MotorDriver.m1Speed;
        case HDLC_M2_SPEED:
            SERIAL_DEBUG.println("HDLC_M2_SPEED");
            out_p->s.d32.ui8[0] = MotorDriver.m2Speed;
            break;
        case HDLC_TEST:
            SERIAL_DEBUG.println("HDLC_TEST");
            out_p->s.d32 = last_post_result;
            break;
        case HDLC_M1_CURR:
            SERIAL_DEBUG.println("HDLC_M1_CURR");
            out_p->s.d32.f = M1Current.value;
            break;
        case HDLC_M2_CURR:
            SERIAL_DEBUG.println("HDLC_M2_CURR");
            out_p->s.d32.f = M2Current.value;
            break;
        case HDLC_STATE:
            SERIAL_DEBUG.println("HDLC_STATE");
            out_p->s.type = HDLC_TYPE_SUCCESS;
            out_p->s.d32.ui8[0] = (uint8_t)GlobalState;
            break;
        case HDLC_FREE_MEM:
            SERIAL_DEBUG.println("HDLC_FREE_MEM");
            out_p->s.d32.ui32 = freeMemory();
            break;
        case HDLC_YAW:
            SERIAL_DEBUG.println("HDLC_YAW");
            out_p->s.d32.ui8[0] = (uint8_t)CamCtrl.read_yaw();
            break;
        case HDLC_PITCH:
            SERIAL_DEBUG.println("HDLC_PITCH");
            out_p->s.d32.ui8[0] = (uint8_t)CamCtrl.read_pitch();
            break;
        case HDLC_WATER_TEMP:
            SERIAL_DEBUG.println("HDLC_WATER_TEMP");
            out_p->s.type = HDLC_TYPE_NOT_IMPLEMENTED;
            break;
        case HDLC_TOTAL_CURR:
            SERIAL_DEBUG.println("HDLC_TOTAL_CURR");
             out_p->s.d32.f = TotalCurrent.value;
            break;
        case HDLC_CRC:
            SERIAL_DEBUG.println("HDLC_TOTAL_CURR");
             out_p->s.d32.ui32 = (uint32_t)CRC;
            break;
        default:
            SERIAL_DEBUG.println("DEFAULT");
            out_p->s.type = HDLC_TYPE_NOT_IMPLEMENTED;
            break;
    }
}

void command_set(packet_t *in_p, packet_t *out_p) {
    SERIAL_DEBUG.print("SET: ");
    SERIAL_DEBUG.println(in_p->s.key);

    out_p->s.type = (uint8_t)HDLC_TYPE_SUCCESS;
    switch (in_p->s.key) {
        case HDLC_TEST:
            SERIAL_DEBUG.println("HDLC_TEST");
            test_mode();
            break;
        case HDLC_M1_SPEED:
            SERIAL_DEBUG.println("HDLC_M1_SPEED");
            if (!MotorDriver.setM1Speed(in_p->s.d32.ui8[0])) {
                out_p->s.type = HDLC_TYPE_FAILURE;
            }
            break;
        case HDLC_M2_SPEED:
            SERIAL_DEBUG.println("HDLC_M2_SPEED");
            if (!MotorDriver.setM2Speed(in_p->s.d32.ui8[0])) {
                out_p->s.type = HDLC_TYPE_FAILURE;
            }
            break;
        case HDLC_YAW:
            SERIAL_DEBUG.println("HDLC_YAW");
            CamCtrl.yaw = in_p->s.d32.ui32;
            break;
        case HDLC_PITCH:
            SERIAL_DEBUG.println("HDLC_PITCH");
            CamCtrl.pitch = in_p->s.d32.ui32;
            break;
        case HDLC_LED:
            SERIAL_DEBUG.println("HDLC_LED");
            led_set(in_p->s.d32.ui32);
            break;
        case HDLC_NET_STATUS:
            SERIAL_DEBUG.println("HDLC_NET_STATUS");
            NetworkStatus.layer1 = in_p->s.d32.ui8[0];
            NetworkStatus.apc = in_p->s.d32.ui8[1];
            NetworkStatus.wan = in_p->s.d32.ui8[2];
            out_p->s.type = HDLC_TYPE_SUCCESS;
            break;
        case HDLC_STATE:
            SERIAL_DEBUG.println("HDLC_STATE");
            out_p->s.type = HDLC_NOT_IMPLEMENTED;
            if (in_p->s.d32.ui8[0] == MCU_STATE_FAULT) {
                fault_handler();
                out_p->s.type = HDLC_TYPE_SUCCESS;
            }
            break;
        default:
            SERIAL_DEBUG.println("DEFAULT");
            out_p->s.type = HDLC_TYPE_NOT_IMPLEMENTED;
            break;
    }
}

void led_set(uint8_t pwm) {
    if (GlobalState != MCU_STATE_FAULT) {
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
  GlobalState = MCU_STATE_FAULT;

  digitalWrite(STBY, LOW);
  CamCtrl.disable();
  MotorDriver.disable();
}

bool test_mode() {
    SERIAL_DEBUG.println("TEST MODE STARTED");
    GlobalState = MCU_STATE_POST;
    /*
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
    */
    last_post_result.ui8[0] = (uint8_t)HDLC_NOT_IMPLEMENTED;
    last_post_result.ui8[1] = (uint8_t)HDLC_NOT_IMPLEMENTED;
    last_post_result.ui8[2] = (uint8_t)HDLC_NOT_IMPLEMENTED;
    GlobalState = MCU_STATE_READY;
    SERIAL_DEBUG.println("TEST MODE ENDED");
    return true;
}
