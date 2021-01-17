#include "def.h"

static netstatus_t NetworkStatus;
TaskHandle_t TaskReadSerial_handle;
TaskHandle_t TaskFaultMonitor_handle;
TaskHandle_t TaskReadSensors_handle;
TaskHandle_t TaskStatus_handle;
TaskHandle_t TaskNetwork_handle;
TaskHandle_t TaskCamera_handle;
TaskHandle_t TaskPOST_handle;

SemaphoreHandle_t interruptSemaphore;

uint8_t GlobalState = MCU_STATUS_INIT;
MC33926Driver MotorDriver(M1IN1, M1IN2, M1PWM, M1FB, M1SF, M2IN1, M2IN2, M2PWM, M2FB, M2SF, EN);
CameraControl CamCtrl(YAW_PIN, YAW_MAX, YAW_MIN, PITCH_PIN, PITCH_MAX, PITCH_MIN, SERVO_DELAY);

Sensor TotalCurrent([]() { return analogRead(CURR_PIN)*(5.0/1024)/66; }, 1); // 66 mV/A
Sensor M1Current([]() { return analogRead(M1SF)*(5.0/1024)/525; }, 1);       // 525 mV/A
Sensor M2Current([]() { return analogRead(M2SF)*(5.0/1024)/525; } , 1);      // 525 mV/A