#!/usr/bin/python

import apc_2016.srv
import rospy

""" Definitions """

srv_name = "rec_obj_srv"

""" Functions """

def callback(req):
    tote_obj_ids = req.tote_obj_ids.split(",")
    obj_id = tote_obj_ids[0]
    rospy.loginfo(srv_name + " request = " + req.tote_obj_ids + ", response = " + obj_id)
    return obj_id

def init():
    rospy.init_node(srv_name + "_node")
    svr = rospy.Service(srv_name, apc_2016.srv.RecObjSrv, callback)
    rospy.loginfo(srv_name + " running...")
    rospy.spin()

""" Entry Point """

if __name__ == "__main__":
    init()
