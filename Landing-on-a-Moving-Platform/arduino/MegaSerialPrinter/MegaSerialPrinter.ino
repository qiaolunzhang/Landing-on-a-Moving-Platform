
/* 
  Scanse Sweep Arduino Library Examples
  
  MegaSerialPrinter:
      - Example sketch for using the Scanse Sweep with the Arduino Mega 2560.
        Collects 3 complete scans, and then prints the sensor readings
      - Assumes Sweep sensor is physically connected to Serial #1 (RX1 & TX1)
        - For the sweep's power, ground, RX & TX pins, follow the connector 
          pinouts in the sweep user manual located here: 
          http://scanse.io/downloads
        - Be sure to connect RX_device -> TX_arduino & TX_device -> RX_arduino
      - For best results, you should provide dedicated external 5V power to the Sweep
        rather than using power from the Arduino. Just be sure to connect the ground 
        from the power source and the arduino. If you are just experimenting, you can
        run the sweep off the 5V power from the Arduino with the Arduino receiving power
        over USB. However this has only been tested with an external powered USB hub. 
        It is possible that using a low power USB port (ex: laptop) to power the 
        arduino & sweep together will result in unexpected behavior. 
      - Note that running off of USB power is not entirely adequate for the sweep, 
        so the quantity and qaulity of sensor readings will drop. This is OK for
        this example, as it is only meant to provide some visual feedback over 
        the serial monitor.
      - In your own projects, be sure to use dedicated power instead of the USB.

  Created by Scanse LLC, February 21, 2017.
  Released into the public domain.
*/

#include <Sweep.h>
#include <Servo.h>

// Create a Sweep device using Serial #1 (RX1 & TX1)
Sweep device(Serial1);

Servo myservo;  // 定义舵机对象，最多八个    
   int pos = 90;    // 定义舵机转动位置 

// keeps track of how many scans have been collected
uint8_t scanCount = 0;
// keeps track of how many samples have been collected
int sampleCount = 0;
bool bleft=0;
bool bright=0;
double safeDis=500;

// Arrays to store attributes of collected scans
bool syncValues[500];         // 1 -> first reading of new scan, 0 otherwise
float angles[500];            // in degrees (accurate to the millidegree)
uint16_t distances[500];      // in cm
uint8_t signalStrengths[500]; // 0:255, higher is better

// Finite States for the program sequence
const uint8_t STATE_WAIT_FOR_USER_INPUT = 0;
const uint8_t STATE_ADJUST_DEVICE_SETTINGS = 1;
const uint8_t STATE_VERIFY_CURRENT_DEVICE_SETTINGS = 2;
const uint8_t STATE_BEGIN_DATA_ACQUISITION = 3;
const uint8_t STATE_GATHER_DATA = 4;
const uint8_t STATE_STOP_DATA_ACQUISITION = 5;
const uint8_t STATE_REPORT_COLLECTED_DATA = 6;
const uint8_t STATE_RESET = 7;
const uint8_t STATE_ERROR = 8;

// Current state in the program sequence
uint8_t currentState;

// String to collect user input over serial
String userInput = "";

void setup()
{
  // Initialize serial
  Serial.begin(9600);    // serial terminal on the computer
  Serial1.begin(115200); // sweep device
  pinMode(22,OUTPUT);
  myservo.attach(9);  // 设置舵机控制针脚
  // reserve space to accumulate user message
  userInput.reserve(50);

  // initialize counter variables and reset the current state
  reset();
}

// Loop functions as an FSM (finite state machine)
void loop()
{
  switch (currentState)
  {
  case STATE_WAIT_FOR_USER_INPUT:
    if (listenForUserInput())
      currentState = STATE_ADJUST_DEVICE_SETTINGS;
    break;
  case STATE_ADJUST_DEVICE_SETTINGS:
    currentState = adjustDeviceSettings() ? STATE_VERIFY_CURRENT_DEVICE_SETTINGS : STATE_ERROR;
    break;
  case STATE_VERIFY_CURRENT_DEVICE_SETTINGS:
    currentState = verifyCurrentDeviceSettings() ? STATE_BEGIN_DATA_ACQUISITION : STATE_ERROR;
    break;
  case STATE_BEGIN_DATA_ACQUISITION:
    currentState = beginDataCollectionPhase() ? STATE_GATHER_DATA : STATE_ERROR;
    break;
  case STATE_GATHER_DATA:
    gatherSensorReading();
    //if (scanCount > 3)
    //  currentState = STATE_STOP_DATA_ACQUISITION;
    break;
  case STATE_STOP_DATA_ACQUISITION:
    currentState = stopDataCollectionPhase() ? STATE_REPORT_COLLECTED_DATA : STATE_ERROR;
    break;
  case STATE_REPORT_COLLECTED_DATA:
    printCollectedData();
    currentState = STATE_RESET;
    break;
  case STATE_RESET:
    Serial.println("\n\nAttempting to reset and run the program again...");
    reset();
    currentState = STATE_WAIT_FOR_USER_INPUT;
    break;
  default: // there was some error
    Serial.println("\n\nAn error occured. Attempting to reset and run program again...");
    reset();
    currentState = STATE_WAIT_FOR_USER_INPUT;
    break;
  }
}

// checks if the user has communicated anything over serial
// looks for the user to send "start"
bool listenForUserInput()
{
  while (Serial.available())
  {
    userInput += (char)Serial.read();
  }
  if (userInput.indexOf("start") != -1)
  {
    Serial.println("Registered user start.");
    return true;
  }
  return false;
}

// Adjusts the device settings
bool adjustDeviceSettings()
{
  // Set the motor speed to 5HZ (codes available from 1->10 HZ)
  bool bSuccess = device.setMotorSpeed(MOTOR_SPEED_CODE_5_HZ);
  Serial.println(bSuccess ? "\nSuccessfully set motor speed." : "\nFailed to set motor speed");

  /*  
  // Device will always default to 500HZ scan rate when it is powered on.
  // Snippet below is left for reference.
  // Set the sample rate to 500HZ (codes available for 500, 750 and 1000 HZ)
  bool bSuccess = device.setSampleRate(SAMPLE_RATE_CODE_500_HZ);
  Serial.println(bSuccess ? "\nSuccessfully set sample rate." : "\nFailed to set sample rate.");
*/
  return bSuccess;
}

// Querries the current device settings (motor speed and sample rate)
// and prints them to the console
bool verifyCurrentDeviceSettings()
{
  // Read the current motor speed and sample rate
  int32_t currentMotorSpeed = device.getMotorSpeed();
  if (currentMotorSpeed < 0)
  {
    Serial.println("\nFailed to get current motor speed");
    return false;
  }
  int32_t currentSampleRate = device.getSampleRate();
  if (currentSampleRate < 0)
  {
    Serial.println("\nFailed to get current sample rate");
    return false;
  }

  // Report the motor speed and sample rate to the computer terminal
  Serial.println("\nMotor Speed Setting: " + String(currentMotorSpeed) + " HZ");
  Serial.println("Sample Rate Setting: " + String(currentSampleRate) + " HZ");

  return true;
}

// Initiates the data collection phase (begins scanning)
bool beginDataCollectionPhase()
{
  // Attempt to start scanning
  Serial.println("\nWaiting for motor speed to stabilize and calibration routine to complete...");
  bool bSuccess = device.startScanning();
  Serial.println(bSuccess ? "\nSuccessfully initiated scanning..." : "\nFailed to start scanning.");
  if (bSuccess)
    Serial.println("\nGathering 3 scans...");
  return bSuccess;
}

// Gathers individual sensor readings until 3 complete scans have been collected
void gatherSensorReading()
{
  // attempt to get the next scan packet
  // Note: getReading() will write values into the "reading" variable
  bool success = false;
  ScanPacket reading = device.getReading(success);
  if (success)
  {
    // check if this reading was the very first reading of a new 360 degree scan
    /*
     * 以下是自己写的代码，根据传感器的信息判断左转还是右转还是跟随GPS巡航
     * 根据在safeDis内第一次检测到障碍的角度判断障碍在斜左方或右方
     * 然后进行左转或右转，如果前方没有障碍物，则22为低电平
     * 22高电平触发继电器，舵机控制线与arduino mega相连
     * 低电平跳回，与pixhawk相连
     * 原理就是根据障碍物左右和有无，进行左转右转与跟随GPS的动作
     * 完成避开障碍物，并保持巡航路线
     */
    if (reading.isSync()){
      //left or right
      for(int i=0;i<sampleCount/4;i++){
        if(distances[i]<=safeDis) bleft=1;
      }
      for(int i=sampleCount/4;i<sampleCount*3/4;i++){
        if(distances[i]<=safeDis) bright=1;
      }
      //make moves
      if(bleft==1 && bright==0){
        //turn left
        digitalWrite(22,HIGH);
        pos=30;
        myservo.write(pos);
        delay(50);
      }
      else if(bleft==0 && bright==1){
        //turn right
        digitalWrite(22,HIGH);
        pos=150;
        myservo.write(pos);
        delay(50);
      }
      else if(bleft==1 && bright==1){
        //stop!!!!!
        digitalWrite(22,HIGH);
        pos=150;
        myservo.write(pos);
        delay(50);
      }
      else{
        digitalWrite(22,LOW);
      }
      //reset for another scan;
      bleft=0;
      bright=0;
      sampleCount=0;   
    }
      //scanCount++;

    // don't collect more than 3 scans
    //if (scanCount > 3)
    //  return;

    // store the info for this sample
    syncValues[sampleCount] = reading.isSync();
    angles[sampleCount] = reading.getAngleDegrees();
    distances[sampleCount] = reading.getDistanceCentimeters();
    signalStrengths[sampleCount] = reading.getSignalStrength();

    // increment sample count
    sampleCount++;
  }
}

// Terminates the data collection phase (stops scanning)
bool stopDataCollectionPhase()
{
  // Attempt to stop scanning
  bool bSuccess = device.stopScanning();

  Serial.println(bSuccess ? "\nSuccessfully stopped scanning." : "\nFailed to stop scanning.");
  return bSuccess;
}

// Prints the collected data to the console
// (only prints the complete scans, ignores the first partial)
void printCollectedData()
{
  Serial.println("\nPrinting info for the collected scans (NOT REAL-TIME):");

  int indexOfFirstSyncReading = 0;
  // don't print the trailing readings from the first partial scan
  while (!syncValues[indexOfFirstSyncReading])
  {
    indexOfFirstSyncReading++;
  }
  // print the readings for all the complete scans
  for (int i = indexOfFirstSyncReading; i < sampleCount; i++)
  {
    if (syncValues[i])
    {
      Serial.println("\n----------------------NEW SCAN----------------------");
    }
    Serial.println("Angle: " + String(angles[i], 3) + ", Distance: " + String(distances[i]) + ", Signal Strength: " + String(signalStrengths[i]));
  }
}

// Resets the variables and state so the sequence can be repeated
void reset()
{
  scanCount = 0;
  sampleCount = 0;
  // reset the sensor
  device.reset();
  delay(50);
  Serial.flush();
  userInput = "";
  Serial.println("\n\nWhenever you are ready, type \"start\" to to begin the sequence...");
  currentState = 0;
}
