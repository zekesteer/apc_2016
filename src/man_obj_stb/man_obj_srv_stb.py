#!/usr/bin/python

import apc_2016.srv
import rospy

""" Definitions """

srv_name = "man_obj_srv"

""" Functions """

def callback(req):
    ack = True
    rospy.loginfo(srv_name + " request = " + str(req.state) + ", response = " + str(ack))
    return ack

def init():
    rospy.init_node(srv_name + "_node")
    svr = rospy.Service(srv_name, apc_2016.srv.ManObjSrv, callback)
    rospy.loginfo(srv_name + " running...")
    rospy.spin()

""" Entry Point """

if __name__ == "__main__":
    init()
