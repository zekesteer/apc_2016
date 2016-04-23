import apc_2016.srv
import rospy

""" Functions """

def init(srv_name):
    rospy.wait_for_service(srv_name)
    global srv    
    srv = rospy.ServiceProxy(srv_name, apc_2016.srv.PosArmSrv)

def set_pose(pose):
    resp = srv(pose)
    return resp.ack

