#!/usr/bin/env python
import apc_2016.srv
import rospy
import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
import tf
import numpy as np

""" Definitions """

srv_name = "pos_arm_srv"

""" Functions """
#global group
def callback(req):
    #global group
    moveit_commander.roscpp_initialize(sys.argv)
  ## Instantiate a RobotCommander object.  This object is an interface to
  ## the robot as a whole.
    robot = moveit_commander.RobotCommander()

  ## Instantiate a PlanningSceneInterface object.  This object is an interface
  ## to the world surrounding the robot.
    scene = moveit_commander.PlanningSceneInterface()

  ## Instantiate a MoveGroupCommander object.  This object is an interface
  ## to one group of joints.  In this case the group is the joints in the left
  ## arm.  This interface can be used to plan and execute motions on the left
  ## arm.
    group = moveit_commander.MoveGroupCommander("manipulator")
    display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path',moveit_msgs.msg.DisplayTrajectory)

    group.set_planner_id('RRTkConfigDefault')
    world_target = req.pose
    #2cm precision
    precision = 0.02
    #1deg precision
    precision_deg = 0.02


    group.clear_pose_targets()
    rospy.loginfo( str(world_target.position.x) +" "+ str(world_target.position.y) +" "+ str(world_target.position.z)+ " "+ str(world_target.orientation.x) + " "+  str(world_target.orientation.y)+ " "+ str(world_target.orientation.z)+" "+  str(world_target.orientation.w) )
    group.set_pose_target(world_target)
    rospy.sleep(5)
    group.go(wait=True)
    rospy.sleep(5)
    current = group.get_current_pose().pose
    flag_sam_pos = (round(world_target.position.x/precision)*precision == round(current.position.x/precision)*precision) and(round(world_target.position.y/precision)*precision == round(current.position.y/precision)*precision) and(round(world_target.position.z/precision)*precision == round(current.position.z/precision)*precision)
    flag_sam_angle = (round(world_target.orientation.x/precision_deg)*precision_deg == round(current.orientation.x/precision_deg)*precision_deg) and(round(world_target.orientation.y/precision_deg)*precision_deg == round(current.orientation.y/precision_deg)*precision_deg) and(round(world_target.orientation.z/precision_deg)*precision_deg == round(current.orientation.z/precision_deg)*precision_deg)and(round(world_target.orientation.w/precision_deg)*precision_deg == round(current.orientation.w/precision_deg)*precision_deg)		
    if flag_sam_pos and flag_sam_angle:
        ack = True
    else:
        ack = False
    moveit_commander.roscpp_shutdown()
    rospy.loginfo(srv_name + " request = " + str(req.pose) + ", response = " + str(ack))

    return ack

def init():
    #global group
    rospy.init_node(srv_name + "_node")

    
	
    #moveit_commander.roscpp_initialize(sys.argv)
  ## Instantiate a RobotCommander object.  This object is an interface to
  ## the robot as a whole.
    #robot = moveit_commander.RobotCommander()

  ## Instantiate a PlanningSceneInterface object.  This object is an interface
  ## to the world surrounding the robot.
    #scene = moveit_commander.PlanningSceneInterface()

  ## Instantiate a MoveGroupCommander object.  This object is an interface
  ## to one group of joints.  In this case the group is the joints in the left
  ## arm.  This interface can be used to plan and execute motions on the left
  ## arm.
    #group = moveit_commander.MoveGroupCommander("manipulator")
    #display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path',moveit_msgs.msg.DisplayTrajectory)
    svr = rospy.Service(srv_name, apc_2016.srv.PosArmSrv, callback)
    rospy.loginfo(srv_name + " running...")
    rospy.spin()

""" Entry Point """

if __name__ == "__main__":
    init()
