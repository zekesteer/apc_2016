import apc_2016.srv
import rospy

""" Functions """

def init(srv_name):
    rospy.wait_for_service(srv_name)
    global srv    
    srv = rospy.ServiceProxy(srv_name, apc_2016.srv.ManObjSrv)

def drop_obj():
    resp = srv(0)
    return resp.ack

def grab_obj():
    resp = srv(1)
    return resp.ack
