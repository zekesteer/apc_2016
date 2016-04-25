#ifndef _ROS_SERVICE_ManObjSrv_h
#define _ROS_SERVICE_ManObjSrv_h
#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include "ros/msg.h"

namespace apc_2016
{

static const char MANOBJSRV[] = "apc_2016/ManObjSrv";

  class ManObjSrvRequest : public ros::Msg
  {
    public:
      bool state;

    ManObjSrvRequest():
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

    const char * getType(){ return MANOBJSRV; };
    const char * getMD5(){ return "001fde3cab9e313a150416ff09c08ee4"; };

  };

  class ManObjSrvResponse : public ros::Msg
  {
    public:
      bool ack;

    ManObjSrvResponse():
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

    const char * getType(){ return MANOBJSRV; };
    const char * getMD5(){ return "8f5729177853f34b146e2e57766d4dc2"; };

  };

  class ManObjSrv {
    public:
    typedef ManObjSrvRequest Request;
    typedef ManObjSrvResponse Response;
  };

}
#endif
