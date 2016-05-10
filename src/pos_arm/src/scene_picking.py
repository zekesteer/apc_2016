#!/usr/bin/env python
import sys
import copy
import rospy
from math import cos, sin, pi
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
import tf
import math
## END_SUB_TUTORIAL

from std_msgs.msg import String

def UR_workcell():
  ## BEGIN_TUTORIAL
  ##
  ## Setup
  ## ^^^^^
  ## CALL_SUB_TUTORIAL imports
  ##
  ## First initialize moveit_commander and rospy.
  print "============ Starting tutorial setup"
  moveit_commander.roscpp_initialize(sys.argv)
  rospy.init_node('workcell',anonymous=True)


  ## Instantiate a PlanningSceneInterface object.  This object is an interface
  ## to the world surrounding the robot.
  scene = moveit_commander.PlanningSceneInterface()

 

 
  group = moveit_commander.MoveGroupCommander("manipulator")
  ## We create this DisplayTrajectory publisher which is used below to publish
  ## trajectories for RVIZ to visualize.
  display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path', moveit_msgs.msg.DisplayTrajectory)
 
  

 ## place obstacles
  #not required
  scene.remove_world_object('table')
  rospy.sleep(10)
  #we r going to do a box that is the neobot
  
  
  pose_c =  geometry_msgs.msg.PoseStamped();
  #both are good
  #pose_c.header.frame_id = '/base_link';
  pose_c.header.frame_id = group.get_planning_frame();
  #pose_c.header.stamp = rospy.Time.now();
  #pose_c.pose= pose1
  pose_c.pose.position.x = 0
  pose_c.pose.position.y =-0.13
 
  pose_c.pose.position.z = 0.775/2 -0.005
 
  print 'draw table'
  scene.add_box('table',pose_c,(0.525, 0.5, 0.775))
  rospy.sleep(10)
  #add shelves

  

  
   
  #add shelves-> these should be behin robot
  scene.remove_world_object('shelf')
  pose_sh =  geometry_msgs.msg.PoseStamped();
  #both are good
  #pose_c.header.frame_id = '/base_link';
  pose_sh.header.frame_id = group.get_planning_frame();
  #pose_c.header.stamp = rospy.Time.now();
  #pose_c.pose= pose1
  pose_sh.pose.position.x = 0.45
  pose_sh.pose.position.y = -1.28
  pose_sh.pose.position.z = 0

  roll = math.pi/2;
  pitch = 0;
  yaw = -3*math.pi/2;
  quaternion = tf.transformations.quaternion_from_euler(roll, pitch, yaw)
  pose_sh.pose.orientation.x = quaternion[0]
  pose_sh.pose.orientation.y = quaternion[1]
  pose_sh.pose.orientation.z = quaternion[2]
  pose_sh.pose.orientation.w = quaternion[3]


  
  scene.add_mesh('shelf',pose_sh,'/home/student/catkin_ws/src/apc_2016/src/pos_arm/meshes/shelves.stl')
  rospy.sleep(10)
  #add tote

  scene.remove_world_object('tote')
  pose_tt =  geometry_msgs.msg.PoseStamped();
  #both are good
  #pose_c.header.frame_id = '/base_link';
  pose_tt.header.frame_id = group.get_planning_frame();
  #pose_c.header.stamp = rospy.Time.now();
  #pose_c.pose= pose1
  pose_tt.pose.position.x = 1
  pose_tt.pose.position.y = -0.46

  pose_tt.pose.position.z = 0
  
  pose_tt.pose.orientation.z =0
  roll = math.pi/2;
  pitch = 0;
  yaw = 0;
  quaternion = tf.transformations.quaternion_from_euler(roll, pitch, yaw)
  pose_tt.pose.orientation.x = quaternion[0]
  pose_tt.pose.orientation.y = quaternion[1]
  pose_tt.pose.orientation.z = quaternion[2]
 
  pose_tt.pose.orientation.w = quaternion[3]

  #scale = (1,1,1)
  scene.add_mesh( 'tote', pose_tt ,'/home/student/catkin_ws/src/apc_2016/src/pos_arm/meshes/tote_s.stl')

  
  moveit_commander.roscpp_shutdown()


  print "============ STOPPING"



if __name__=='__main__':
  try:
    UR_workcell()
  except rospy.ROSInterruptException:
    pass
