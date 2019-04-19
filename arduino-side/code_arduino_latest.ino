#include <Arduino_FreeRTOS.h>
#include <Arduino.h>
#include <stdlib.h>
#include <task.h>
#include <Wire.h>

#define STACK_SIZE 200


#define SensorHigh (0x1D) //Sensor1 Register
#define SensorLow (0x53) //Sensor2 Register
byte _buff1[6];

char POWER_CTL = 0x2D;     //Power Control Register
char DATA_FORMAT = 0x31;   //Calibrate ADXL345
char DATAX0 = 0x32;        //X-Axis Data 0
char DATAX1 = 0x33;        //X-Axis Data 1
char DATAY0 = 0x34;        //Y-Axis Data 0
char DATAY1 = 0x35;        //Y-Axis Data 1
char DATAZ0 = 0x36;        //Z-Axis Data 0
char DATAZ1 = 0x37;        //Z-Axis Data 1
int initialData[9];

//Power 
const int CURRENT_SENSOR_PIN = A4;  // Input pin for measuring Vout
const int VOLTAGE_SENSOR_PIN = A0;
const int VOLTAGE_REF = 5;  // Reference voltage for analog read
float currentSensorValue;   // Variable to store value from analog read
float voltageSensorValue;
float current = 0;       // Calculated current value
float voltage = 0;

//Handshake variables 
int val = 0;
int handshake = 0;
int ack = 0;

//Message buffer
char sendBuffer[4000];

void setup() {
  // put your setup code here, to run once:
  Wire.begin();
  Serial.begin(115200);
  Serial3.begin(115200);
  pinMode(A1, OUTPUT);
  pinMode(A2, OUTPUT);
  pinMode(A3, OUTPUT);
  establishHandshake();
  resetSensors();
  //getReading(initialData);  
  xTaskCreate(mainTask, "mainTask", STACK_SIZE, NULL, 3, NULL);
  vTaskStartScheduler();
}

void establishHandshake(){

  Serial.println("Awaiting handshake.");
  
  while(handshake < 2){
      while(handshake == 0){
        if(Serial3.available()){
          val = Serial3.read();
          if(val == 48){
            Serial.println("Sending ACK to Raspberry Pi.");
            Serial3.write("1");
            handshake = 1;
            val = 0;
          }
        }
      }
      while (handshake == 1){
        if(Serial3.available()){
          Serial3.write("1");
          val = Serial3.read();
          Serial.println(val);
          if(val == 49){
            Serial.println("Received ACK of Raspberry Pi.");
            handshake = 2;
          }
        }
        else {
          Serial3.write("1");
          Serial.println("serial3 not available");
        }
      }
  }
  
  if (handshake == 2){
    Serial.println("Handshake Established.");
  }
}

void convertReading(int readings[]){

  int x1, y1, z1;
  int x2, y2, z2;
  int x3, y3, z3;
  int checksum = 0;
  char checksum_char[7];
  char char_x1[7], char_y1[7], char_z1[7];
  char char_x2[7], char_y2[7], char_z2[7];
  char char_x3[7], char_y3[7], char_z3[7];
  char char_voltage[7], char_current[7];

  currentSensorValue = analogRead(CURRENT_SENSOR_PIN);
  currentSensorValue = (currentSensorValue * VOLTAGE_REF) / 1023;
  current = (currentSensorValue * 1000) / (1.2 * 10000);
  current = round(current * 10.0)/10.0;
  voltageSensorValue = analogRead(VOLTAGE_SENSOR_PIN);
  voltage =  2 * (voltageSensorValue * VOLTAGE_REF) / 1023;
  voltage = round(voltage * 10.0)/10.0;
  
  int csVoltage = (int) (voltage * 10.0);
  int csCurrent = (int) (current * 10.0);
  
  x1 = readings[0];
  checksum ^= x1;
  y1 = readings[1];
  checksum ^= y1;
  z1 = readings[2];
  checksum ^= z1;
  
  x2 = readings[3];
  checksum ^= x2;
  y2 = readings[4];
  checksum ^= y2;
  z2 = readings[5];
  checksum ^= z2;

  x3 = readings[6];
  checksum ^= x3;
  y3 = readings[7];
  checksum ^= y3;
  z3 = readings[8];
  checksum ^= z3;

  checksum ^= csVoltage;
  checksum ^= csCurrent;
  
  strcat(sendBuffer, "#");
  
  dtostrf(x1, 1, 0, char_x1);
  strcat(sendBuffer, char_x1);
  strcat(sendBuffer, ",");
  
  dtostrf(y1, 1, 0, char_y1);
  strcat(sendBuffer, char_y1);
  strcat(sendBuffer, ",");
  
  dtostrf(z1, 1, 0, char_z1);
  strcat(sendBuffer, char_z1);
  strcat(sendBuffer, ",");
  strcat(sendBuffer, "|");

  dtostrf(x2, 1, 0, char_x2);
  strcat(sendBuffer, char_x2);
  strcat(sendBuffer, ",");
  
  dtostrf(y2, 1, 0, char_y2);
  strcat(sendBuffer, char_y2);
  strcat(sendBuffer, ",");
  
  dtostrf(z2, 1, 0, char_z2);
  strcat(sendBuffer, char_z2);
  strcat(sendBuffer, ",");
  strcat(sendBuffer, "|");

  dtostrf(x3, 1, 0, char_x3);
  strcat(sendBuffer, char_x3);
  strcat(sendBuffer, ",");
  
  dtostrf(y3, 1, 0, char_y3);
  strcat(sendBuffer, char_y3);
  strcat(sendBuffer, ",");
  
  dtostrf(z3, 1, 0, char_z3);
  strcat(sendBuffer, char_z3);
  strcat(sendBuffer, ",");
  strcat(sendBuffer, "|");

  //dtostrf(dummyVoltage, 1, 1, char_voltage);
  dtostrf(voltage, 1, 1, char_voltage);
  strcat(sendBuffer, char_voltage);
  strcat(sendBuffer, "|");

  //dtostrf(dummyCurrent, 1, 1, char_current);
  dtostrf(current, 1, 1, char_current);
  strcat(sendBuffer, char_current);
  strcat(sendBuffer, "|");
  
  dtostrf(checksum, 1, 0, checksum_char);
  strcat(sendBuffer, checksum_char);
  strcat(sendBuffer, "|");
  strcat(sendBuffer, "\n");
  
  Serial.println(sendBuffer);
 
  delay(28);
}

void resetSensors() {

  Serial.println("beginning");
  digitalWrite(A1, LOW);
  digitalWrite(A2, LOW);
  digitalWrite(A3, HIGH);
  wakeDevice(SensorHigh); 
  digitalWrite(A1, LOW);
  digitalWrite(A2, HIGH);
  digitalWrite(A3, LOW);
  wakeDevice(SensorHigh);
  digitalWrite(A1, HIGH);
  digitalWrite(A2, LOW);
  digitalWrite(A3, LOW);
  wakeDevice(SensorHigh); 
}

void wakeDevice(int device) {
  Wire.beginTransmission(device);
  Wire.write(POWER_CTL);
  Wire.write(8);
  Wire.endTransmission(); //this segment resets the Power Control Register and sets it to read mode
  Wire.beginTransmission(device);
  Wire.write(DATA_FORMAT);
  Wire.write(0x01); //change this as necessary
  Wire.endTransmission();
}

void readFrom(int device, byte address, int num, byte _buff[]) {
  Wire.beginTransmission(device);
  Wire.write(address);
  Wire.endTransmission();

  Wire. beginTransmission(device);
  Wire.requestFrom(device, num);

  int i = 0;
  while(Wire.available()) {
    _buff[i] = Wire.read();
    i++;
  }
  Wire.endTransmission();
}

void getReading(int values[]) {
  uint8_t howManyBytesToRead = 6;
  digitalWrite(A1, LOW);
  digitalWrite(A2, LOW);
  digitalWrite(A3, HIGH);
  
  readFrom(SensorHigh, DATAX0, howManyBytesToRead, _buff1);
  
  values[0] = (((int)_buff1[1] << 8) | _buff1[0]);
  values[1] = (((int)_buff1[3] << 8) | _buff1[2]);
  values[2] = (((int)_buff1[5] << 8) | _buff1[4]);
  memset(_buff1, 0, sizeof(_buff1));
  
  digitalWrite(A1, LOW);
  digitalWrite(A2, HIGH);
  digitalWrite(A3, LOW);
  
  readFrom(SensorHigh, DATAX0, howManyBytesToRead, _buff1);
  
  values[3] = (((int)_buff1[1] << 8) | _buff1[0]);
  values[4] = (((int)_buff1[3] << 8) | _buff1[2]);
  values[5] = (((int)_buff1[5] << 8) | _buff1[4]);
  memset(_buff1, 0, sizeof(_buff1));

  digitalWrite(A1, HIGH);
  digitalWrite(A2, LOW);
  digitalWrite(A3, LOW);
  
  readFrom(SensorHigh, DATAX0, howManyBytesToRead, _buff1);
  
  values[6] = (((int)_buff1[1] << 8) | _buff1[0]);
  values[7] = (((int)_buff1[3] << 8) | _buff1[2]);
  values[8] = (((int)_buff1[5] << 8) | _buff1[4]);
  memset(_buff1, 0, sizeof(_buff1));
}

void mainTask(void *p){ 

  TickType_t xLastWakeTime;
  xLastWakeTime = xTaskGetTickCount();
  
  while(1){
    //Empty buffer
    strcpy(sendBuffer, "");
    int readings [9]; //x1, y1, z1, x2, y2, z2, x3, y3, z3 respectively
    getReading(readings);
    for(int x = 0; x<9; x++) {
      //readings[x] -= initialData[x];
      readings[x] *=100;
      readings[x] /= 256;
    }
    //Serial.println((String)"x1 : " + readings[0] + " y1 : " + readings[1] + " z1: " + readings[2] + " x2: " + readings[3] + " y2: " + readings[4] + " z2: " + readings[5] + " x3: " + readings[6] + " y3: " + readings[7] + " z3: " + readings[8]); //and so on
    convertReading(readings);
    Serial3.write(sendBuffer);
  }
}

void loop() {}
