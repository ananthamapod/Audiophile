/************************* IMPORTS *************************/

#include <Wire.h>
#include <Adafruit_MotorShield.h>

/***********************************************************/


/************************* GLOBALS *************************/

// Create the motor shield object with the default I2C address
//Adafruit_MotorShield AFMS = Adafruit_MotorShield(); 
// Or, create it with a different I2C address (say for stacking)
// Adafruit_MotorShield AFMS = Adafruit_MotorShield(0x61); 

// Select which 'port' M1, M2, M3 or M4. In this case, M1
//Adafruit_DCMotor *leftMotor = AFMS.getMotor(1);
// You can also make another motor on port M3
//Adafruit_DCMotor *rightMotor = AFMS.getMotor(3);

const int pingPinLeft = 5;
const int pingPinFront = 7;
const int pingPinRight = 9;
long distanceLeft = 0;
long distanceFront = 0;
long distanceRight = 0;
String instr;
const int ledPin = 13;
const int leftPin = 4;
const int rightPin = 3;

/***********************************************************/


void setup()
{
  //AFMS.begin();
  
  // Set the speed to start, from 0 (off) to 255 (max speed)
  leftMotor->setSpeed(0);
  rightMotor->setSpeed(0);
  // turn on motor
  leftMotor->run(RELEASE);
  rightMotor->run(RELEASE);

  pinMode(ledPin, OUTPUT);
  // initialize serial communications at a 9600 baud rate
  Serial.begin(9600);
  establishContact();
}

void loop()
{
  if(Serial.available()) {
    instr = Serial.readString();
    //move(instr);
  }
  
  Serial.print(distanceLeft);
  Serial.print(" ");
  Serial.print(distanceFront);
  Serial.print(" ");
  Serial.println(distanceRight);
  //wait 100 milliseconds so we don't drive themselves crazy
  distanceLeft = microsecondsToInches(ping(pingPinLeft));
  distanceFront = microsecondsToInches(ping(pingPinFront));
  distanceRight = microsecondsToInches(ping(pingPinRight));
  delay(300);
}

/************************ UTILITIES ************************/

void establishContact() {
  while (Serial.available() <= 0) {
  Serial.println('A');   // send a capital A
  delay(300);
  }
}

void move(String instr) {
  String[] tmp = instr.split(" ");
  String op = tmp[0];
  double val = (double) tmp[1];
  // Both sides move forward at the same rate
  // Speed set at moderate, not maximum
  if(instr.equals("FORWARD")) {
    leftMotor->setSpeed(100);
    rightMotor->setSpeed(100);
    leftMotor->run(FORWARD);
    rightMotor->run(FORWARD);
  }

  // Turns on the tank thread principle
  // One side moves forward, the other side moves backward
  // Turning is set at a slower speed for precision
  else if(instr.equals("LEFT")) {
    leftMotor->setSpeed(60);
    rightMotor->setSpeed(60);
    leftMotor->run(BACKWARD);
    rightMotor->run(FORWARD);
  }

  // Turns on the tank thread principle
  // One side moves forward, the other side moves backward
  // Turning is set at a slower speed for precision
  else if(instr.equals("RIGHT")) {
    leftMotor->setSpeed(60);
    rightMotor->setSpeed(60);
    leftMotor->run(FORWARD);
    rightMotor->run(BACKWARD);
  }

  // Comes to a stop
  // Speed comes to zero
  else if(instr.equals("STOP")) {
    leftMotor->setSpeed(0);
    rightMotor->setSpeed(0);
    leftMotor->run(RELEASE);
    rightMotor->run(RELEASE);
  }
}

//These are modified from from built-in Ping example

long ping(int pingPin) {
  // Send out ping
  // Triggered by HIGH pulse of at least 2 microseconds
  // Bound with LOW pulses to ensure clean HIGH pulse
  pinMode(pingPin, OUTPUT);
  digitalWrite(pingPin, LOW);
  delayMicroseconds(2);
  digitalWrite(pingPin, HIGH);
  delayMicroseconds(5);
  digitalWrite(pingPin, LOW);
 
 // Read ping time
 pinMode(pingPin, INPUT);
 return pulseIn(pingPin, HIGH);
}

/* According to Parallax's datasheet for the PING))), there are 
73.746 microseconds per inch (i.e. sound travels at 1130 feet per second).
This gives the distance travelled by the ping, outbound and return, so we 
divide by 2 to get the distance of the obstacle. */
long microsecondsToInches(long microseconds)
{
  return microseconds / 74 / 2;
}

/* The speed of sound is 340 m/s or 29 microseconds per centimeter. 
The ping travels out and back, so to find the distance of the object 
we take half of the distance travelled. */
long microsecondsToCentimeters(long microseconds)
{
  return microseconds / 29 / 2;
}

/***********************************************************/
