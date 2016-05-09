#include <ros.h>
#include <Servo.h> 
#include <apc_2016/ManObjSrv.h>
#include <apc_2016/SnsObjSrv.h>
#include <apc_2016/WghObjSrv.h>

int servo1 = 9;
int buttonPin = 2;
int loadCell = A2;                //output from load cell
int numReadings = 10;

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

void callback2(const apc_2016::SnsObjSrv::Request &request, apc_2016::SnsObjSrv::Response &response)
{
	int pressSwitch = digitalRead(8);
	response.state = (pressSwitch == 1);  
	delay(100);
}

void callback3(const apc_2016::WghObjSrv::Request &request, apc_2016::WghObjSrv::Response &response)
{
    int readings = 0;
    for (int i = 0; i < numReadings; i++)
        readings += analogRead(loadCell);

	response.weight = (short)(readings / numReadings);
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
/*
ros::ServiceServer<apc_2016::SnsObjSrv::Request, apc_2016::SnsObjSrv::Response> server2("sns_obj_srv", &callback2);
ros::ServiceServer<apc_2016::WghObjSrv::Request, apc_2016::WghObjSrv::Response> server3("wgh_obj_srv", &callback3);
*/
void setup()
{
  pinMode(8,INPUT);
  pinMode(13, OUTPUT); 

  nh.getHardware()->setBaud(115200);
  nh.initNode();
  nh.advertiseService(server1);
/*  nh.advertiseService(server2);
  nh.advertiseService(server3);*/
	  
  Serial.begin(9600);
  servo.attach(servo1); //OUTPUT pin
}

void loop()
{
   nh.spinOnce();
   delay(1);
}

