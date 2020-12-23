#include <hdlc_def.h>
#include <redis_def.h>
#include <avr/wdt.h>
#include <Arduhdlc.h>
#include <DualMC33926MotorShield.h>
#include <SparkFun_TB6612.h>
#include <Arduino_FreeRTOS.h>
#include <semphr.h>

// Pin assignment
#define M1DIR 7
#define M1PWM 9 //changing this with use analog read instead of timer
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
  MCUSR = 0; // restore from SW reset
  InitKeys();

  //Pin def
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(, INPUT);

  //Serial
  Serial.begin(PORT_SPEED);
  while(!Serial); //Wait for serial to become available

  //Motor driver
  md.init();
  
  //RTOS
  xTaskCreate(TaskReadSerial, "Read Serial", 128, NULL, 3, &TaskReadSerial_handler);
  xTaskCreate(TaskReadSensors, "Read Sensors", 128, NULL, 1, &TaskReadSensors_handler);

  interruptSemaphore = xSemaphoreCreateBinary();
 if (interruptSemaphore != NULL) {
    //Attach interrupt for Arduino digital pin
    attachInterrupt(digitalPinToInterrupt(2), interruptHandler, HIGH);
  }
}

void loop(){}

void interruptHandler() {
  xSemaphoreGiveFromISR(interruptSemaphore, NULL);
}

void TaskReadSerial(void *pvParameters) {
  for (;;) {
    while(Serial.available()>0) {
      //Serial.println("Reading port");
      char rx = char(Serial.read());
      hdlc.charReceiver(rx);
    }
     vTaskDelay(1); 
  }
}

void TaskReadSensors(void *pvParameters) {
  for(;;) {
    unsigned int m1 = md.getM1CurrentMilliamps();
    vTaskDelay( 1000 / portTICK_PERIOD_MS ); //delay 1000 ms
  }
}

void CommandHandler(Packet packet) {
  packet_t response;
  response.id = packet.id;
  response.type = HDLC_TYPE_RESP;

  if (packet.type == HDLC_TYPE_SET) {
    
  } else if (packet.type == HDLC_TYPE_GET) {

  } else {
    GlobalState = HDLC_STATUS_FAULT;
  }
  response.data[0].value = GlobalState;
  buffer_t out_buffer;
  out_buffer.packet = response;
  hdlc.sendFrame((uint8_t *)&out_buffer.bytes, sizeof(out_buffer.bytes));
}

//Function to send out one 8bit character
void send_character(uint8_t data)
{
  Serial.print((char)data);
}

//Frame handler function. What to do with received data?
void hdlc_frame_handler(const uint8_t *data, uint16_t length)
{
  buffer_t buffer;
  for (int i=0; i < length; i++) {
    buffer.bytes[i] = data[i];
    //dataBuffer.bytes[i] = data[i];
  }
  CommandHandler(buffer.packet);
}

void reboot() {
  wdt_enable(WDTO_15MS);
  for(;;) { 
    // do nothing and wait
  } 
}