#!/usr/bin/env python

import pos_arm
import geometry_msgs
import rospy

# bin poses

bin_a_pose = geometry_msgs.msg.Pose()
bin_a_pose.position.x = 0.30
bin_a_pose.position.y = -1.17
bin_a_pose.position.z = 1.62
bin_a_pose.orientation.w = 0.71
bin_a_pose.orientation.x = 0.00
bin_a_pose.orientation.y = 3.37
bin_a_pose.orientation.z = -0.71

bin_b_pose = geometry_msgs.msg.Pose()
bin_b_pose.position.x = -0.01
bin_b_pose.position.y = -1.17
bin_b_pose.position.z = 1.62
bin_b_pose.orientation.w = 0.71
bin_b_pose.orientation.x = 0.00
bin_b_pose.orientation.y = 5.96
bin_b_pose.orientation.z = -0.71

bin_c_pose = geometry_msgs.msg.Pose()
bin_c_pose.position.x = -0.28
bin_c_pose.position.y = -1.16
bin_c_pose.position.z = 1.62
bin_c_pose.orientation.w = 0.71
bin_c_pose.orientation.x = 0.00
bin_c_pose.orientation.y = 0.00
bin_c_pose.orientation.z = -0.71

bin_d_pose = geometry_msgs.msg.Pose()
bin_d_pose.position.x = 0.30
bin_d_pose.position.y = -1.17
bin_d_pose.position.z = 1.30
bin_d_pose.orientation.w = 0.71
bin_d_pose.orientation.x = 0.00
bin_d_pose.orientation.y = 0.00
bin_d_pose.orientation.z = -0.71

bin_e_pose = geometry_msgs.msg.Pose()
bin_e_pose.position.x = -0.02
bin_e_pose.position.y = -1.22
bin_e_pose.position.z = 1.29
bin_e_pose.orientation.w = 0.72
bin_e_pose.orientation.x = 0.00
bin_e_pose.orientation.y = 4.01
bin_e_pose.orientation.z = -0.69

bin_f_pose = geometry_msgs.msg.Pose()
bin_f_pose.position.x = -0.32
bin_f_pose.position.y = -1.17
bin_f_pose.position.z = 1.29
bin_f_pose.orientation.w = 0.71
bin_f_pose.orientation.x = 0.00
bin_f_pose.orientation.y = 0.00
bin_f_pose.orientation.z = -0.71

bin_g_pose = geometry_msgs.msg.Pose()
bin_g_pose.position.x = 0.30
bin_g_pose.position.y = -1.17
bin_g_pose.position.z = 0.97
bin_g_pose.orientation.w = 0.71
bin_g_pose.orientation.x = 0.00
bin_g_pose.orientation.y = 0.00
bin_g_pose.orientation.z = -0.71

bin_h_pose = geometry_msgs.msg.Pose()
bin_h_pose.position.x = 0.00
bin_h_pose.position.y = -1.17
bin_h_pose.position.z = 0.97
bin_h_pose.orientation.w = 0.71
bin_h_pose.orientation.x = 0.00
bin_h_pose.orientation.y = 0.00
bin_h_pose.orientation.z = 0.71

bin_i_pose = geometry_msgs.msg.Pose()
bin_i_pose.position.x = -0.31
bin_i_pose.position.y = -1.16
bin_i_pose.position.z = 0.97
bin_i_pose.orientation.w = 0.71
bin_i_pose.orientation.x = 0.00
bin_i_pose.orientation.y = 0.00
bin_i_pose.orientation.z = -0.71

# observe pose

observe_obj_pose = geometry_msgs.msg.Pose()
observe_obj_pose.position.x = 0.767387000929
observe_obj_pose.position.y = 0.122699071207
observe_obj_pose.position.z = 0.556378909004
observe_obj_pose.orientation.w = 0.703878595009
observe_obj_pose.orientation.x =  -0.0177689692122
observe_obj_pose.orientation.y = 0.709154400105
observe_obj_pose.orientation.z = 0.0365954099967

# pick pose

pick_obj_pose = geometry_msgs.msg.Pose()
pick_obj_pose.position.x = 0.77
pick_obj_pose.position.y = 0.12
pick_obj_pose.position.z = 0.1
pick_obj_pose.orientation.w =  0.703878595
pick_obj_pose.orientation.x = -0.017768969
pick_obj_pose.orientation.y =  0.709154
pick_obj_pose.orientation.z = 0.0365954099

# recognise pose

rec_obj_pose = geometry_msgs.msg.Pose()
rec_obj_pose.position.x = 0.26
rec_obj_pose.position.y = -0.30
rec_obj_pose.position.z = 1.16
rec_obj_pose.orientation.w = 0.57
rec_obj_pose.orientation.x = 0.51
rec_obj_pose.orientation.y = 0.58
rec_obj_pose.orientation.z = -0.41

# weigh pose

weigh_obj_pose = geometry_msgs.msg.Pose()
weigh_obj_pose.position.x = 0.83
weigh_obj_pose.position.y = 0.10
weigh_obj_pose.position.z = 1.50
weigh_obj_pose.orientation.w = 1.00
weigh_obj_pose.orientation.x = 0.00
weigh_obj_pose.orientation.y = 0.00
weigh_obj_pose.orientation.z = 0.02


def init():
    rospy.init_node("tsk_pln_tst_node")
    pos_arm.init("pos_arm_srv")

    result = pos_arm.set_pose(observe_obj_pose)

    rospy.loginfo("Task planner test: " + str(result))

    rospy.spin()

if __name__ == "__main__":
    init()
