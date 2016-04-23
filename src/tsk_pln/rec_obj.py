import apc_2016.srv
import rospy

""" Functions """

def init(srv_name):
    rospy.wait_for_service(srv_name)
    global srv    
    srv = rospy.ServiceProxy(srv_name, apc_2016.srv.RecObjSrv)

def get_obj_id(obj_ids):
    data = ",".join(obj_ids)
    resp = srv(data)
    return resp.obj_id
