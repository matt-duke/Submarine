#include <hdlc_def.h>
#include <redis_def.h>
#include <Arduhdlc.h>
#include <DualMC33926MotorShield.h>
#include <SparkFun_TB6612.h>
#include <Arduino_FreeRTOS.h>
#include <semphr.h>

#include "sensors.h"

// Serial port defs
#define SERIAL Serial
#define SERIAL_DEBUG Serial1

// Pin assignment
#define M1DIR 7
#define M1PWM 9 //changing this will use analog read instead of timer
#define M1FB A0
#define M2DIR 8
#define M2PWM 10
#define M2FB A1
#define nD2 4
#define nSF 12

#define AIN1 12
#define BIN1 17
#define AIN2 14
#define BIN2 18
#define PWMA 15
#define PWMB 16
#define STBY 19

const int offsetA = 1;
const int offsetB = 1;

#define BTN_PIN 20

//Variables
TaskHandle_t TaskReadSerial_handler;
TaskHandle_t TaskReadSensors_handler;

SemaphoreHandle_t interruptSemaphore; // For button press

DualMC33926MotorShield md(M1DIR, M1PWM, M1FB, M2DIR, M2PWM, M2FB, nD2, nSF);
Motor LED(AIN1, AIN2, PWMA, offsetA, STBY);

buffer_t GlobalBuffer;
uint8_t GlobalState = HDLC_STATUS_OK;

// Function prototypes
void send_character(uint8_t data);
void hdlc_frame_handler(const uint8_t *data, uint16_t length);

void TaskReadSerial(void *pvParameters);
void TaskReadSensors(void *pvParameters);

Arduhdlc hdlc(&send_character, &hdlc_frame_handler, MAX_HDLC_FRAME_LENGTH);
void setup(){
  //Internal
  InitKeys();

  //Pin def
  pinMode(LED_BUILTIN, OUTPUT);

  //Serial
  SERIAL_DEBUG.begin(9600);
  SERIAL.begin(PORT_SPEED);
  while(!SERIAL); //Wait for serial to become available

  //Motor driver
  md.init();
  
  //FREE_RTOS
  xTaskCreate(TaskReadSerial, "Read Serial", 128, NULL, 3, &TaskReadSerial_handler);
  //xTaskCreate(TaskReadSensors, "Read Sensors", 128, NULL, 1, &TaskReadSensors_handler);

  interruptSemaphore = xSemaphoreCreateBinary();
 if (interruptSemaphore != NULL) {
    //Attach interrupt for Arduino digital pin
    attachInterrupt(digitalPinToInterrupt(2), interruptHandler, HIGH);
  }
  SERIAL_DEBUG.println("Booted up.");
}

void loop(){}

void interruptHandler() {
  xSemaphoreGiveFromISR(interruptSemaphore, NULL);
}

void TaskReadSerial(void *pvParameters) {
  for (;;) {
    if (SERIAL.available()>0) {
      SERIAL_DEBUG.println("Reading serial buffer...");
    } else {
      continue;
    }
    while(SERIAL.available()>0) {
      char rx = SERIAL.read();
      SERIAL_DEBUG.print("Received: ");
      SERIAL_DEBUG.println(rx, BIN);
      hdlc.charReceiver(rx);
    }
    SERIAL_DEBUG.println("Done reading...");
    vTaskDelay(1); 
  }
}

void TaskReadSensors(void *pvParameters) {
  for(;;) {
    SERIAL_DEBUG.println("Updating sensors");
    unsigned int m1 = md.getM1CurrentMilliamps();
    vTaskDelay( 1000 / portTICK_PERIOD_MS ); //delay 1000 ms
  }
}

void CommandHandler(Packet packet) {
  SERIAL_DEBUG.println("received packet");
  /*packet_t response;
  response.id = packet.id;
  response.type = packet.type;

  if (packet.type == HDLC_TYPE_SET) {
    
  } else if (packet.type == HDLC_TYPE_GET) {
    
  } else {
    GlobalState = HDLC_STATUS_FAULT;
  }
  response.data.value = GlobalState;*/
  buffer_t out_buffer;
  out_buffer.packet.id = packet.id;
  hdlc.sendFrame((uint8_t *)&out_buffer.bytes, sizeof(out_buffer.bytes));
}

//Function to send out one 8bit character
void send_character(uint8_t data)
{
  SERIAL.print((char)data);
}

//Frame handler function. What to do with received data?
void hdlc_frame_handler(const uint8_t *data, uint16_t length)
{
  SERIAL_DEBUG.println("frame_handler");
  buffer_t buffer;
  for (int i=0; i < length; i++) {
    buffer.bytes[i] = data[i];
  }
  CommandHandler(buffer.packet);
}