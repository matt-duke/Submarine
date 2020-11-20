#include <Arduino_FreeRTOS.h>
#include <Arduhdlc.h>
#include "hdlc_def.h"
#include "redis_def.h"


TaskHandle_t serialHandler;
TaskHandle_t sensorHandler;

Buffer dataBuffer;

byte status = STATUS_NONE;

bool LED_STATE = 0;

/* Function to send out byte/char */
void send_character(uint8_t data);

/* Function to handle a valid HDLC frame */
void hdlc_frame_handler(const uint8_t *data, uint16_t length);

/* Initialize Arduhdlc library with three parameters.
1. Character send function, to send out HDLC frame one byte at a time.
2. HDLC frame handler function for received frame.
3. Length of the longest frame used, to allocate buffer in memory */
Arduhdlc hdlc(&send_character, &hdlc_frame_handler, MAX_HDLC_FRAME_LENGTH);

/* Function to send out one 8bit character */
void send_character(uint8_t data)
{
    Serial.print((char)data);
}

/* Frame handler function. What to do with received data? */
void hdlc_frame_handler(const uint8_t *data, uint16_t length)
{
    //hdlc.sendFrame(data, PACKET_SIZE);
    for (int i=0; i < length; i++) {
      dataBuffer.bytes[i] = data[i];
    }

    switch(dataBuffer.packet.type) {
      case COMMAND_ERROR: ErrorHandler(dataBuffer.packet); break;
      case COMMAND_SET_MOTOR: CommandMotor(dataBuffer.packet); break;
      case COMMAND_SET_LED: CommandLed(dataBuffer.packet); break;
      case COMMAND_STATUS: CommandStatus(dataBuffer.packet); break;
      default: hdlc.sendFrame(dataBuffer.bytes, PACKET_SIZE); break;
    }
}

void setup(){

  pinMode(LED_BUILTIN, OUTPUT);

  Serial.begin(9600);
  
  xTaskCreate(
    ReadSerial,
    "Read Serial",
    128,
    NULL,
    3,
    &serialHandler );

  xTaskCreate(
    ReadSensors,
    "Read Sensors",
    128,
    NULL,
    1,
    &sensorHandler );

  digitalWrite(LED_BUILTIN, LOW);
  
  InterruptInit();

  status = STATUS_OK;
}


ISR(TIMER3_COMPA_vect)
{  
  BaseType_t xHigherPriorityTaskWoken = pdFALSE;
  vTaskNotifyGiveFromISR(serialHandler, &xHigherPriorityTaskWoken);
  if (xHigherPriorityTaskWoken) {
    taskYIELD();
  }
}

ISR(TIMER4_COMPA_vect)
{  
  BaseType_t xHigherPriorityTaskWoken = pdFALSE;
  vTaskNotifyGiveFromISR(sensorHandler, &xHigherPriorityTaskWoken);
  if (xHigherPriorityTaskWoken) {
    taskYIELD();
  }
}


void loop(){}

void InterruptInit()
{
  //https://www.instructables.com/id/Arduino-Timer-Interrupts/
  
  cli();

  //set timer1 interrupt at 5Hz
  TCCR3A = 0;// set entire TCCR1A register to 0
  TCCR3B = 0;// same for TCCR1B
  TCNT3  = 0;//initialize counter value to 0
  // set compare match register for 1hz increments
  OCR3A = 3124;// = (16*10^6) / (5*1024) - 1 (must be <65536) SERIAL
  // turn on CTC mode
  TCCR3B |= (1 << WGM12);
  // Set CS10 and CS12 bits for 1024 prescaler
  TCCR3B |= (1 << CS12) | (1 << CS10);  
  // enable timer compare interrupt
  TIMSK3 |= (1 << OCIE3A);

  //set timer2 interrupt at 1kHz
  TCCR4A = 0;// set entire TCCR2A register to 0
  TCCR4B = 0;// same for TCCR2B
  TCNT4  = 0;//initialize counter value to 0
  // set compare match register for 8khz increments
  OCR4A = 31249;// = (16*10^6) / (0.5*1024) - 1 (must be <65536) SENSOR
  // turn on CTC mode
  TCCR4A |= (1 << WGM12);
  // Set CS10 and CS12 bits for 1024 prescaler
  TCCR4B |= (1 << CS12) | (1 << CS10);  
  // enable timer compare interrupt
  TIMSK4 |= (1 << OCIE4A);
  
  sei();
}

void ReadSerial(void *pvParameters) {

  for (;;) {
    if (ulTaskNotifyTake(pdTRUE, portMAX_DELAY)) {
      //Serial.println("Reading port");
      char rx = char(Serial.read());
      hdlc.charReceiver(rx);
    }
  }
}

void ReadSensors(void *pvParameters) {
  for(;;) {
    if (ulTaskNotifyTake(pdTRUE, portMAX_DELAY)) {
      
    }
  }
}

void CommandMotor(Packet packet) {
  // Update motor values
  if (packet.id == ID_MOTOR_L) {
    
  }
  else if (packet.id == ID_MOTOR_R) {
    
  }
  else{
    //print error
  }
}

void CommandLed(Packet packet) {
  if (packet.id == ID_HEADLIGHT) {
    
  }
  else if (packet.id = ID_BUILT_IN_LED) {
    bool state = packet.data.bytes[3];
    digitalWrite(LED_BUILTIN, state);
  }
  else {
    //print error
  }
}

void ErrorHandler(Packet packet) {
  //trigger safety features, ie. disable motors
}

void CommandStatus(Packet packet) {
  digitalWrite(LED_BUILTIN, HIGH);
  byte resp[PACKET_SIZE];
  resp[0] = COMMAND_STATUS;
  resp[1] = status;
  hdlc.sendFrame(resp, PACKET_SIZE);
}
