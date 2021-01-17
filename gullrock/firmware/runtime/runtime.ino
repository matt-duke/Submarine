#include <hdlc_def.h>
#include <Arduhdlc.h>
#include <Arduino_FreeRTOS.h>
#include <Adafruit_NeoPixel.h>

#include "command_handler.h"
#include "def.h"

// Functions
void send_character(uint8_t data);
void hdlc_frame_handler(const uint8_t *data, uint16_t length);

packet_t GlobalBuffer = {};

Adafruit_NeoPixel status(1, LED_STATUS, NEO_RGB + NEO_KHZ800);
Arduhdlc hdlc(&send_character, &hdlc_frame_handler, MAX_HDLC_FRAME_LENGTH);

// Function prototypes
void send_character(uint8_t data);
void hdlc_frame_handler(const uint8_t *data, uint16_t length);

void TaskReadSerial(void *pvParameters);
void TaskReadSensors(void *pvParameters);
void TaskStatus(void *pvParameters);
void TaskNetwork(void *pvParameters);
void TaskCamera(void *pvParameters);
void TaskPOST(void *pvParameters);
void TaskFaultMonitor(void *pvParameters);

void setup(){
  GlobalState = MCU_STATUS_INIT;

  //Turn off status LED
  status.setPixelColor(0,0,0,0);
  status.show();

  //Pin modes
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(LED_STATUS, OUTPUT);
  //pinMode(LED_ETH, OUTPUT);
  pinMode(CURR_PIN, INPUT);
  //Serial
  SERIAL_DEBUG.begin(9600);
  SERIAL_DEBUG.println("Running setup.");
  SERIAL.begin(PORT_SPEED);
  while(!SERIAL); //Wait for serial to become available

  status.setPixelColor(0, 0, 0, 0);
  status.show();
  setup_external();
  
  //FREE_RTOS
  //xTaskCreate(TaskStatus, "Status LED", 128, NULL, 2, &TaskStatus_handle);
  //xTaskCreate(TaskNetwork, "Network LED", 128, NULL, 2, &TaskNetwork_handle);
  //xTaskCreate(TaskCamera, "Update camera", 128, NULL, 1, &TaskCamera_handle);
  //xTaskCreate(TaskReadSensors, "Read sensors", 128, NULL, 3, &TaskReadSensors_handle);
  //xTaskCreate(TaskPOST, "Startup test", 128, NULL, 2, &TaskPOST_handle);
  xTaskCreate(TaskReadSerial, "Read serial", 128, NULL, 1, &TaskReadSerial_handle);
  //xTaskCreate(TaskFaultMonitor, "Monitor errors", 128, NULL, 2, &TaskFaultMonitor_handle);

  interruptSemaphore = xSemaphoreCreateBinary();
  if (interruptSemaphore != NULL) {
    //Attach interrupt for Arduino digital pin
    attachInterrupt(digitalPinToInterrupt(2), interruptHandler, HIGH);
  }

  //RUN POST
  //xTaskNotifyGive(TaskPOST_handle);
  vTaskStartScheduler();
}

void loop(){}

void TaskPOST(void *pvParameters) {
  static uint32_t thread_notification;

  for (;;) {
    thread_notification = ulTaskNotifyTake(pdTRUE, portMAX_DELAY);
    if (thread_notification) {
      if (test_mode()) {
        GlobalState = MCU_STATUS_OK;
      }
    }
  }
}

void TaskFaultMonitor(void *pvParameters) {
  for (;;) {
    bool fault = false;
    if (MotorDriver.getM1Fault()) {
      SERIAL_DEBUG.println("M1 Fault");
    }
    if (MotorDriver.getM2Fault()) {
      SERIAL_DEBUG.println("M2 Fault");
    }
    if (fault) {
      fault_handler();
    }
    vTaskDelay( 1000 / portTICK_PERIOD_MS ); 
  }
}

void interruptHandler() {
  xSemaphoreGiveFromISR(interruptSemaphore, NULL);
  portYIELD_FROM_ISR(); //?
}

void TaskReadSerial(void *pvParameters) {
  for (;;) {
    //SERIAL_DEBUG.println("Checking buffer...");
    if (SERIAL.available()>0) {
      //SERIAL_DEBUG.println("Reading serial buffer...");
    } else {
      continue;
    }
    while(SERIAL.available()>0) {
      uint8_t rx = (uint8_t) SERIAL.read();
      SERIAL_DEBUG.print("Received: ");
      SERIAL_DEBUG.println(rx, DEC);
      hdlc.charReceiver(rx);
    }
    //SERIAL_DEBUG.println("Done reading...");
    vTaskDelay(1); 
  }
}

void TaskReadSensors(void *pvParameters) {
  for(;;) {
    TotalCurrent.read();
    M1Current.read();
    M2Current.read();
    //SERIAL_DEBUG.println(TotalCurrent.value);
    vTaskDelay( 1000 / portTICK_PERIOD_MS ); //delay 1000 ms
  }
}

void TaskStatus(void *pvParameters) {
  int strobe = 0;
  bool add = true;
  colour_t ColourProfiles[MCU_NUM_STATUS];
  ColourProfiles[MCU_STATUS_INIT] = (colour_t){20,0,80,50};
  ColourProfiles[MCU_STATUS_FAULT] = (colour_t){100,0,0,40};
  ColourProfiles[MCU_STATUS_POST] = (colour_t){60,0,85,25};
  ColourProfiles[MCU_STATUS_OK] = (colour_t){0,100,20,0}; 

  for(;;) {
    colour_t c = ColourProfiles[GlobalState];

    if (c.rate != 0) {
      float mult = float(strobe)/100;
      status.setPixelColor(0, c.r*mult, c.g*mult, c.b*mult);
      if (strobe >= 100) {
        add = false;
      } else if (strobe <= 0) {
        add = true;
      }
      if (add) {
        strobe += 1;
      } else {
        strobe -= 1;
      }
    } else {
      status.setPixelColor(0, c.r, c.g, c.b);
    }
    status.show();
    int rate = 1000;
    if (c.rate < rate) {
      rate = c.rate;
    } 
    vTaskDelay( rate / portTICK_PERIOD_MS ); 
  }
}

void TaskNetwork(void *pvParameters) {
  uint8_t i = 0;
  bool add = true;
  int rate = 1000;
  for (;;) {
    if (!NetworkStatus.layer1) {
      i++;
    }
    else if (!NetworkStatus.apc) {
      // strobe effect
      if (i == 255 || i == 0) add = !add;
      (add) ? i++ : i--;
    }
    else if (NetworkStatus.wan) {
      i = 255;
    }
    analogWrite(LED_ETH, i);
    vTaskDelay(rate / portTICK_PERIOD_MS); 
  }
}

void TaskCamera(void *pvParameters) {
  for (;;) {
    if (!CamCtrl.on_target()) {
      SERIAL_DEBUG.println("Updating camera...");
      while (!CamCtrl.on_target()) {
        CamCtrl.update();
        vTaskDelay(1);
      }
      SERIAL_DEBUG.println("Finished updating camera.");
    }
    vTaskDelay( 10 / portTICK_PERIOD_MS); // delay 10 ms
  }
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

  packet_t in_p = {};
  packet_t out_p = {};
  for (int i=0; i < length; i++) {
    in_p.bytes[i] = data[i];
  }
  out_p.s.id = in_p.s.id;

  SERIAL_DEBUG.print("received packet id: ");
  SERIAL_DEBUG.println(out_p.s.id);
  if (0 != command_handler(&in_p, &in_p)) {
    fault_handler();
  }
  hdlc.sendFrame((uint8_t *)&out_p.bytes, sizeof(out_p.bytes));
}
