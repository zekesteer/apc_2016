#!/usr/bin/python

import apc_2016.srv
import rospy
import std_msgs
import numpy

""" Definitions """

pub_name = "dep_obj_pub"
srv_name = "dep_obj_srv"
sub_name = "dep_obj_sub"

positions = { }

""" Functions """

def get_dis(pos1_x, pos1_y, pos1_z, pos2_x, pos2_y, pos2_z):
    return numpy.sqrt(numpy.power(pos1_x - pos2_x, 2) + numpy.power(pos1_y - pos2_y, 2) + numpy.power(pos1_z - pos2_z, 2))

def sub_callback(data):
    global positions
    points = data.data.split(";")

    for i in range(0, len(points)):
        point = points[i]
        if point != "":
            coords = point.split(",")
            center_x = int(coords[0])
            center_y = int(coords[1])
            center_z = int(coords[2])

            min_key = None
            min_dis = 100000
            for key in positions.keys():
                dis = get_dis(key[0], key[1], key[2], center_x, center_y, center_z)
                if min_key == None or min_dis > dis:
                    min_key = key
                    min_dis = dis

            if min_key == None or min_dis > 20:
                positions[(center_x, center_y, center_z)] = 1
            else:
                new_center_x = (min_key[0] + center_x) / 2
                new_center_y = (min_key[1] + center_y) / 2
                new_center_z = (min_key[2] + center_z) / 2
                weight = positions[min_key] + 1
                del positions[min_key]
                positions[(new_center_x, new_center_y, new_center_z)] = weight
                

    if len(positions) > 1000:
        positions = { }

            #rospy.loginfo("received coord: x " + str(center_x) + ", y " + str(center_y)) 
    # todo; track weights, etc.

def srv_callback(req):
    global positions
    
    max_key = None
    for key in positions.keys():
        if max_key == None or positions[max_key] < positions[key]:
            max_key = key 

    if max_key == None:
       pos = ""
    else:
        pos = str(max_key[0]) + "," + str(max_key[1]) + "," + str(max_key[2])

    rospy.loginfo(srv_name + " request = , response = " + pos)
    return pos

def init():
    rospy.init_node(sub_name + "_node")
    rospy.Subscriber(pub_name, std_msgs.msg.String, sub_callback)
    svr = rospy.Service(srv_name, apc_2016.srv.DepObjSrv, srv_callback)
    rospy.loginfo(srv_name + " running...")
    rospy.spin()

""" Entry Point """

if __name__ == "__main__":
    init()
