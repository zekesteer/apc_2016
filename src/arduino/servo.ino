#include <ros.h>
#include <Servo.h> 
#include <apc_2016/ManObjSrv.h>

ros::NodeHandle nh;
Servo servo;

void callback(const apc_2016::ManObjSrv::Request &request, apc_2016::ManObjSrv::Response &response)
{
  if (request.state)
  {
    servo.write(180); //set servo angle, valve is open corresponds to 180 deg??
    digitalWrite(13, HIGH - digitalRead(13));  //toggle led when valve is open 
  }
  else
  {
    servo.write(90); //set servo angle, valve is close corresponds to 90 deg??
    digitalWrite(13, LOW); // turn-off led if valve is close
  }

  delay(2); // wait for valve to open/close before returning
  response.ack = true;
}

ros::ServiceServer<apc_2016::ManObjSrv::Request, apc_2016::ManObjSrv::Response> server("man_obj_srv", &callback);

void setup()
{
  pinMode(13, OUTPUT); 
  nh.initNode();
  nh.advertiseService(server);   
  servo.attach(8); //OUTPUT pin
}

void loop()
{
   nh.spinOnce();
   delay(1);
}

