/************************* IMPORTS *************************/

#include <Wire.h>
#include <Adafruit_MotorShield.h>

/***********************************************************/


/************************* GLOBALS *************************/

// Create the motor shield object with the default I2C address
Adafruit_MotorShield AFMS = Adafruit_MotorShield(); 
// Or, create it with a different I2C address (say for stacking)
// Adafruit_MotorShield AFMS = Adafruit_MotorShield(0x61); 

// Select which 'port' M1, M2, M3 or M4. In this case, M1
Adafruit_DCMotor *leftMotor = AFMS.getMotor(1);
// You can also make another motor on port M3
Adafruit_DCMotor *rightMotor = AFMS.getMotor(3);

const int pingPinLeft = 5;
const int pingPinFront = 7;
const int pingPinRight = 9;
long distanceLeft = 0;
long distanceFront = 0;
long distanceRight = 0;
String instr;
const int leftPin = 4;
const int rightPin = 3;

/***********************************************************/


void setup()
{
  AFMS.begin();
  
  // Set the speed to start, from 0 (off) to 255 (max speed)
  leftMotor->setSpeed(0);
  rightMotor->setSpeed(0);
  // turn on motor
  leftMotor->run(RELEASE);
  rightMotor->run(RELEASE);

  // initialize serial communications at a 9600 baud rate
  Serial.begin(9600);
  establishContact();
}

void loop()
{
  if(Serial.available()) {
    String op  = Serial.readStringUntil(' ');
    //Serial.read(); //next character is comma, so skip it using this  
    String value  = Serial.readStringUntil('\n');
    //Serial.read();
    move(op, value);
  }
  
  Serial.print(distanceLeft);
  Serial.print(" ");
  Serial.print(distanceFront);
  Serial.print(" ");
  Serial.println(distanceRight);
  //wait 300 milliseconds for now because we don't need unnecessarily large amounts of sensor data
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

void move(String op, String value) {
  //String tmp[] = instr.split(" ");
  //String op = tmp[0];
  int val = value.toInt();
  // Both sides move forward at the same rate
  // Speed set at moderate, not maximum
  if(op.equals("FORWARD")) {
    leftMotor->setSpeed(val);
    rightMotor->setSpeed(val);
    leftMotor->run(FORWARD);
    rightMotor->run(FORWARD);
  }

  // Turns on the tank thread principle
  // One side moves forward, the other side moves backward
  // Turning is set at a slower speed for precision
  else if(op.equals("LEFT")) {
    leftMotor->setSpeed(val);
    rightMotor->setSpeed(val);
    leftMotor->run(BACKWARD);
    rightMotor->run(FORWARD);
  }

  // Turns on the tank thread principle
  // One side moves forward, the other side moves backward
  // Turning is set at a slower speed for precision
  else if(op.equals("RIGHT")) {
    leftMotor->setSpeed(val);
    rightMotor->setSpeed(val);
    leftMotor->run(FORWARD);
    rightMotor->run(BACKWARD);
  }

  // Comes to a stop
  // Speed comes to zero
  else if(op.equals("STOP")) {
    leftMotor->setSpeed(0);
    rightMotor->setSpeed(0);
    leftMotor->run(RELEASE);
    rightMotor->run(RELEASE);
  }
  
  else if(op.equals("TEST")) {
    leftMotor->setSpeed(140);
    leftMotor->run(FORWARD); 
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
