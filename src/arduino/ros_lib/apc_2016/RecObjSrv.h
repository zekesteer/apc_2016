#ifndef _ROS_SERVICE_RecObjSrv_h
#define _ROS_SERVICE_RecObjSrv_h
#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include "ros/msg.h"

namespace apc_2016
{

static const char RECOBJSRV[] = "apc_2016/RecObjSrv";

  class RecObjSrvRequest : public ros::Msg
  {
    public:
      const char* tote_obj_ids;

    RecObjSrvRequest():
      tote_obj_ids("")
    {
    }

    virtual int serialize(unsigned char *outbuffer) const
    {
      int offset = 0;
      uint32_t length_tote_obj_ids = strlen(this->tote_obj_ids);
      memcpy(outbuffer + offset, &length_tote_obj_ids, sizeof(uint32_t));
      offset += 4;
      memcpy(outbuffer + offset, this->tote_obj_ids, length_tote_obj_ids);
      offset += length_tote_obj_ids;
      return offset;
    }

    virtual int deserialize(unsigned char *inbuffer)
    {
      int offset = 0;
      uint32_t length_tote_obj_ids;
      memcpy(&length_tote_obj_ids, (inbuffer + offset), sizeof(uint32_t));
      offset += 4;
      for(unsigned int k= offset; k< offset+length_tote_obj_ids; ++k){
          inbuffer[k-1]=inbuffer[k];
      }
      inbuffer[offset+length_tote_obj_ids-1]=0;
      this->tote_obj_ids = (char *)(inbuffer + offset-1);
      offset += length_tote_obj_ids;
     return offset;
    }

    const char * getType(){ return RECOBJSRV; };
    const char * getMD5(){ return "76017c4f57a3cba63fa126fd416eaab8"; };

  };

  class RecObjSrvResponse : public ros::Msg
  {
    public:
      const char* obj_id;

    RecObjSrvResponse():
      obj_id("")
    {
    }

    virtual int serialize(unsigned char *outbuffer) const
    {
      int offset = 0;
      uint32_t length_obj_id = strlen(this->obj_id);
      memcpy(outbuffer + offset, &length_obj_id, sizeof(uint32_t));
      offset += 4;
      memcpy(outbuffer + offset, this->obj_id, length_obj_id);
      offset += length_obj_id;
      return offset;
    }

    virtual int deserialize(unsigned char *inbuffer)
    {
      int offset = 0;
      uint32_t length_obj_id;
      memcpy(&length_obj_id, (inbuffer + offset), sizeof(uint32_t));
      offset += 4;
      for(unsigned int k= offset; k< offset+length_obj_id; ++k){
          inbuffer[k-1]=inbuffer[k];
      }
      inbuffer[offset+length_obj_id-1]=0;
      this->obj_id = (char *)(inbuffer + offset-1);
      offset += length_obj_id;
     return offset;
    }

    const char * getType(){ return RECOBJSRV; };
    const char * getMD5(){ return "92426bd0785e0b4655ae981c76b9de6b"; };

  };

  class RecObjSrv {
    public:
    typedef RecObjSrvRequest Request;
    typedef RecObjSrvResponse Response;
  };

}
#endif
