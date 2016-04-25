#ifndef _ROS_SERVICE_SnsObjSrv_h
#define _ROS_SERVICE_SnsObjSrv_h
#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include "ros/msg.h"

namespace apc_2016
{

static const char SNSOBJSRV[] = "apc_2016/SnsObjSrv";

  class SnsObjSrvRequest : public ros::Msg
  {
    public:

    SnsObjSrvRequest()
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

    const char * getType(){ return SNSOBJSRV; };
    const char * getMD5(){ return "d41d8cd98f00b204e9800998ecf8427e"; };

  };

  class SnsObjSrvResponse : public ros::Msg
  {
    public:
      bool state;

    SnsObjSrvResponse():
      state(0)
    {
    }

    virtual int serialize(unsigned char *outbuffer) const
    {
      int offset = 0;
      union {
        bool real;
        uint8_t base;
      } u_state;
      u_state.real = this->state;
      *(outbuffer + offset + 0) = (u_state.base >> (8 * 0)) & 0xFF;
      offset += sizeof(this->state);
      return offset;
    }

    virtual int deserialize(unsigned char *inbuffer)
    {
      int offset = 0;
      union {
        bool real;
        uint8_t base;
      } u_state;
      u_state.base = 0;
      u_state.base |= ((uint8_t) (*(inbuffer + offset + 0))) << (8 * 0);
      this->state = u_state.real;
      offset += sizeof(this->state);
     return offset;
    }

    const char * getType(){ return SNSOBJSRV; };
    const char * getMD5(){ return "001fde3cab9e313a150416ff09c08ee4"; };

  };

  class SnsObjSrv {
    public:
    typedef SnsObjSrvRequest Request;
    typedef SnsObjSrvResponse Response;
  };

}
#endif
