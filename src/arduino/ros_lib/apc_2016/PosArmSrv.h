#ifndef _ROS_SERVICE_PosArmSrv_h
#define _ROS_SERVICE_PosArmSrv_h
#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include "ros/msg.h"
#include "geometry_msgs/Pose.h"

namespace apc_2016
{

static const char POSARMSRV[] = "apc_2016/PosArmSrv";

  class PosArmSrvRequest : public ros::Msg
  {
    public:
      geometry_msgs::Pose pose;

    PosArmSrvRequest():
      pose()
    {
    }

    virtual int serialize(unsigned char *outbuffer) const
    {
      int offset = 0;
      offset += this->pose.serialize(outbuffer + offset);
      return offset;
    }

    virtual int deserialize(unsigned char *inbuffer)
    {
      int offset = 0;
      offset += this->pose.deserialize(inbuffer + offset);
     return offset;
    }

    const char * getType(){ return POSARMSRV; };
    const char * getMD5(){ return "f192399f711a48924df9a394d37edd67"; };

  };

  class PosArmSrvResponse : public ros::Msg
  {
    public:
      bool ack;

    PosArmSrvResponse():
      ack(0)
    {
    }

    virtual int serialize(unsigned char *outbuffer) const
    {
      int offset = 0;
      union {
        bool real;
        uint8_t base;
      } u_ack;
      u_ack.real = this->ack;
      *(outbuffer + offset + 0) = (u_ack.base >> (8 * 0)) & 0xFF;
      offset += sizeof(this->ack);
      return offset;
    }

    virtual int deserialize(unsigned char *inbuffer)
    {
      int offset = 0;
      union {
        bool real;
        uint8_t base;
      } u_ack;
      u_ack.base = 0;
      u_ack.base |= ((uint8_t) (*(inbuffer + offset + 0))) << (8 * 0);
      this->ack = u_ack.real;
      offset += sizeof(this->ack);
     return offset;
    }

    const char * getType(){ return POSARMSRV; };
    const char * getMD5(){ return "8f5729177853f34b146e2e57766d4dc2"; };

  };

  class PosArmSrv {
    public:
    typedef PosArmSrvRequest Request;
    typedef PosArmSrvResponse Response;
  };

}
#endif
