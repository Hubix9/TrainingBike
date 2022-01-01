#define USB_CFG_DEVICE_NAME     'P','o','t','a','t','o','B','i','k','e'
#define USB_CFG_DEVICE_NAME_LEN 10

#include <DigiUSB.h>

unsigned long currentTime = 0;
unsigned long previousRotationTime = 0;

void setup() {
  // put your setup code here, to run once:
  DigiUSB.begin(); 
  pinMode(5, INPUT);
  pinMode(1, OUTPUT);
  pinMode(2, INPUT);
  pinMode(0,INPUT);
  //digitalWrite(0, LOW);
  digitalWrite(1, HIGH);
  //digitalWrite(5, LOW);
  //digitalWrite(2, LOW);
  currentTime = millis(); 
  previousRotationTime = currentTime;
}

float wheelLength = 0.0055;
int kmh = 0;
int previousKmh = 0;
int previousControllerValue = 0;
int previousWheelValue = 0;

void loop() {
  DigiUSB.refresh();
  currentTime = millis();
  int controllerValue = analogRead(1); // Controllers pin
  int wheelValue = digitalRead(0); // Wheel pin
  //Controller stuff
  if (controllerValue > 1000) {
    // Don't turn
    controllerValue = 2; 
    } 
  else if (controllerValue > 500) {
    // Turn left
    controllerValue = 1; 
  } 
  else {
    // Turn right
    controllerValue = 0; 
  }
  //=======================
  

  if (previousWheelValue == 1 && wheelValue == 0) {
      int timeDelta = currentTime - previousRotationTime;
      kmh = 3600000 / timeDelta * wheelLength + 1;
      previousRotationTime = currentTime;
  }
  
  //Timeout when no rotation is detected
  if (currentTime > previousRotationTime + 1.5 * 1000) {
      if (kmh > 0) {
        kmh = kmh - 1;
      }
  } 

  

  if (kmh != previousKmh || controllerValue != previousControllerValue) {
      DigiUSB.print('!'); // Beginning of a packet
      DigiUSB.print(controllerValue);
      DigiUSB.print('/');
      DigiUSB.print(kmh);
      DigiUSB.print('$');  
  }
 
  previousKmh = kmh;
  previousWheelValue = wheelValue;
  previousControllerValue = controllerValue; 
  DigiUSB.delay(1);
}
