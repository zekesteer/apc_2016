#ifndef _ROS_SERVICE_WghObjSrv_h
#define _ROS_SERVICE_WghObjSrv_h
#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include "ros/msg.h"

namespace apc_2016
{

static const char WGHOBJSRV[] = "apc_2016/WghObjSrv";

  class WghObjSrvRequest : public ros::Msg
  {
    public:

    WghObjSrvRequest()
    {
    }

    virtual int serialize(unsigned char *outbuffer) const
    {
      int offset = 0;
      return offset;
    }

    virtual int deserialize(unsigned char *inbuffer)
    {
      int offset = 0;
     return offset;
    }

    const char * getType(){ return WGHOBJSRV; };
    const char * getMD5(){ return "d41d8cd98f00b204e9800998ecf8427e"; };

  };

  class WghObjSrvResponse : public ros::Msg
  {
    public:
      int16_t weight;

    WghObjSrvResponse():
      weight(0)
    {
    }

    virtual int serialize(unsigned char *outbuffer) const
    {
      int offset = 0;
      union {
        int16_t real;
        uint16_t base;
      } u_weight;
      u_weight.real = this->weight;
      *(outbuffer + offset + 0) = (u_weight.base >> (8 * 0)) & 0xFF;
      *(outbuffer + offset + 1) = (u_weight.base >> (8 * 1)) & 0xFF;
      offset += sizeof(this->weight);
      return offset;
    }

    virtual int deserialize(unsigned char *inbuffer)
    {
      int offset = 0;
      union {
        int16_t real;
        uint16_t base;
      } u_weight;
      u_weight.base = 0;
      u_weight.base |= ((uint16_t) (*(inbuffer + offset + 0))) << (8 * 0);
      u_weight.base |= ((uint16_t) (*(inbuffer + offset + 1))) << (8 * 1);
      this->weight = u_weight.real;
      offset += sizeof(this->weight);
     return offset;
    }

    const char * getType(){ return WGHOBJSRV; };
    const char * getMD5(){ return "d2d45ad5d93883ebc15497846bb06278"; };

  };

  class WghObjSrv {
    public:
    typedef WghObjSrvRequest Request;
    typedef WghObjSrvResponse Response;
  };

}
#endif
