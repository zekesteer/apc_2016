import apc_2016.srv
import rospy

""" Functions """

def init(srv_name):
    rospy.wait_for_service(srv_name)
    global srv    
    srv = rospy.ServiceProxy(srv_name, apc_2016.srv.SnsObjSrv)

def is_obj_sns():
    resp = srv()
    return resp.is_sns
