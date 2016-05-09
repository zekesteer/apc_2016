#!/usr/bin/python

import apc_2016.srv
import random
import rospy

""" Definitions """

srv_name = "wgh_obj_srv"

""" Functions """

def callback(req):
    weight = random.random() * 1000
    rospy.loginfo(srv_name + " request =, response = " + str(weight))
    return weight

def init():
    rospy.init_node(srv_name + "_node")
    svr = rospy.Service(srv_name, apc_2016.srv.WghObjSrv, callback)
    rospy.loginfo(srv_name + " running...")
    rospy.spin()

""" Entry Point """

if __name__ == "__main__":
    init()
