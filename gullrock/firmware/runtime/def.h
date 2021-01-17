#pragma once

#include <Arduino.h>
#include <hdlc_def.h>
#include <Arduino_FreeRTOS.h>
#include <semphr.h>
#include <CameraControl.h>
#include <MC33926Driver.h>
#include <Sensors.h>

// Function macros

#define SERIAL Serial
#define SERIAL_DEBUG Serial1

// Pin assignment
#define M1IN1 10
#define M1IN2 11
#define M1PWM 9
#define M1FB A7
#define M1SF 8
#define M2IN1 36
#define M2IN2 34
#define M2PWM 7
#define M2FB A6
#define M2SF 6
#define EN 32

#define AIN1 49
#define BIN1 40
#define AIN2 47
#define BIN2 42
#define PWMA 45
#define PWMB 44
#define STBY 51
#define EXP_LED_CURR 0.1

#define BTN_PIN 20
#define LED_ETH 21
#define LED_STATUS 4

#define CURR_PIN A15

#define SERVO_DELAY 25 //delay, higher=slower, ms
#define YAW_PIN 2
#define YAW_MAX 100
#define YAW_MIN 65
#define PITCH_PIN 3
#define PITCH_MAX 160
#define PITCH_MIN 90

struct colour_t {
  uint8_t r;
  uint8_t g;
  uint8_t b;
  uint16_t rate; //blink rate, ms
};

struct netstatus_t {
    bool layer1;
    bool apc;
    bool wan;
};

extern netstatus_t NetworkStatus;
extern TaskHandle_t TaskReadSerial_handle;
extern TaskHandle_t TaskFaultMonitor_handle;
extern TaskHandle_t TaskReadSensors_handle;
extern TaskHandle_t TaskStatus_handle;
extern TaskHandle_t TaskNetwork_handle;
extern TaskHandle_t TaskCamera_handle;
extern TaskHandle_t TaskPOST_handle;

extern SemaphoreHandle_t interruptSemaphore; // For button press

extern uint8_t GlobalState;
extern MC33926Driver MotorDriver;
extern CameraControl CamCtrl;

#define BUFFER_SIZE 10
extern Sensor TotalCurrent;
extern Sensor M1Current;
extern Sensor M2Current;
