#!/usr/bin/python

import apc_2016.srv
import collections
import numpy
import rospy
import std_msgs

""" Definitions """

pub_name = "dep_obj_pub"
srv_name = "dep_obj_srv"
sub_name = "dep_obj_sub"

positions = collections.deque(maxlen=20)

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

            min_pos = None
            min_dis = 100000
            for j in range(0, len(positions)):
                pos = positions[j]
                dis = get_dis(pos[0], pos[1], pos[2], center_x, center_y, center_z)
                if min_pos == None or min_dis > dis:
                    min_pos = pos
                    min_dis = dis

            if min_pos == None or min_dis > 50:
                positions.append((center_x, center_y, center_z, 1))
            else:
                new_center_x = (min_pos[0] + center_x) / 2
                new_center_y = (min_pos[1] + center_y) / 2
                new_center_z = (min_pos[2] + center_z) / 2
                weight = min_pos[3] + 1
                positions.remove(min_pos)
                positions.append((new_center_x, new_center_y, new_center_z, weight))
                
            #rospy.loginfo("received coord: x " + str(center_x) + ", y " + str(center_y)) 
    # todo; track weights, etc.

def srv_callback(req):
    global positions
    
    max_pos = -1
    for i in range(0, len(positions)):
        pos = positions[i]
        if max_pos < 0 or max_pos[3] < positions[i][3]:
            max_pos = pos

    if max_pos < 0:
       pos = ""
    else:
        pos = str(max_pos[0]) + "," + str(max_pos[1]) + "," + str(max_pos[2])

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
