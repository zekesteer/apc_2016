#!/usr/bin/python

import apc_2016.srv
import random
import rospy

""" Definitions """

srv_name = "dep_obj_srv"

""" Functions """
def callback(req):
    pos_x = 256 + (random.random() - 0.5) * 256
    pos_y = 212 + (random.random() - 0.5) * 212
    rospy.loginfo(srv_name + " request = , response = " + pos_x + "," + pos_y)
    return pos

def init():
    rospy.init_node(srv_name + "_node")
    svr = rospy.Service(srv_name, apc_2016.srv.DepObjSrv, callback)
    rospy.loginfo(srv_name + " running...")
    rospy.spin()

""" Entry Point """

if __name__ == "__main__":
    init()
