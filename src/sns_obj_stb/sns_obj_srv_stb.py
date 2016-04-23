#!/usr/bin/python

import apc_2016.srv
import random
import rospy

""" Definitions """

srv_name = "sns_obj_srv"

""" Functions """

def callback(req):
    is_sns = random.random() < 0.5
    rospy.loginfo(srv_name + " request =, response = " + str(is_sns))
    return is_sns

def init():
    rospy.init_node(srv_name + "_node")
    svr = rospy.Service(srv_name, apc_2016.srv.SnsObjSrv, callback)
    rospy.loginfo(srv_name + " running...")
    rospy.spin()

""" Entry Point """

if __name__ == "__main__":
    init()
