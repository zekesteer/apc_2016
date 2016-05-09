#include <ros.h>
#include <Servo.h> 
#include <apc_2016/ManObjSrv.h>
#include <apc_2016/SnsObjSrv.h>
#include <apc_2016/WghObjSrv.h>

int servo1 = 9;
int buttonPin = 2;
int loadCell = A2;                //output from load cell
int analogValue = 0;
const int numReadings = 10;      //determines the number of values in the rolling average
int readings[numReadings];      // the readings from the analog input
int index = 0;                  // the index of the current reading
int total = 0;                  // the running total
int rollingAverage = 0;         // the rolling average reading
int pressSwitch = 0;
int xPosition = 0;
int yPosition = 0;
int buttonState = 0;
int servoVal;


ros::NodeHandle nh;
Servo servo;

void callback1(const apc_2016::ManObjSrv::Request &request, apc_2016::ManObjSrv::Response &response)
{
  if (request.state)
    open();
  else
    close();

  delay(2000); // wait for valve to open/close before returning
  response.ack = true;  
}


void rollingReading() {

 total= total - readings[index];              // subtract the last reading   

 readings[index] = analogRead(loadCell);      // read from the sensor

 total= total + readings[index];             // add the reading to the total:      

 index = index + 1;                          // advance to the next position in the array:

 if (index >= numReadings)                  // if we're at the end of the array wrap around to the beginning

 index = 0;                           

 rollingAverage = total / numReadings;         
  

 delay(1);                              // delay in between reads for stability            

}


void callback2(const apc_2016::SnsObjSrv::Request &request, apc_2016::SnsObjSrv::Response &response)
{
	pinMode(8,INPUT);
	pressSwitch = digitalRead(8);
	
	response.state = (pressSwitch == 1);  
	
	delay(100);
}


void callback3(const apc_2016::WghObjSrv::Request &request, apc_2016::WghObjSrv::Response &response)
{
	rollingReading();
	
	response.weight = (short)rollingAverage;
	delay(1); 
}


void open()
{
  servo.write(180); //set servo angle, valve is open corresponds to 180 deg??
  digitalWrite(13, HIGH - digitalRead(13));  //toggle led when valve is open 
}

void close()
{
  servo.write(90); //set servo angle, valve is close corresponds to 90 deg??
  digitalWrite(13, LOW); // turn-off led if valve is close
}

ros::ServiceServer<apc_2016::ManObjSrv::Request, apc_2016::ManObjSrv::Response> server1("man_obj_srv", &callback1);
ros::ServiceServer<apc_2016::SnsObjSrv::Request, apc_2016::SnsObjSrv::Response> server2("sns_obj_srv", &callback2);
ros::ServiceServer<apc_2016::WghObjSrv::Request, apc_2016::WghObjSrv::Response> server3("wgh_obj_srv", &callback3);


void setup()
{
  pinMode(13, OUTPUT); 

  nh.getHardware()->setBaud(115200);
  nh.initNode();
  nh.advertiseService(server1);
  nh.advertiseService(server2);
  nh.advertiseService(server3);
	  
  Serial.begin(9600);
  servo.attach(servo1); //OUTPUT pin
  
  for (int thisReading = 0; thisReading < numReadings; thisReading++)    //This need to be in the set-up section to aviod resetting the array in the loop
  readings[thisReading] = 0.0;  
}

void loop()
{
   nh.spinOnce();
   delay(1);
}

