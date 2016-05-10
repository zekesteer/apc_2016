#!/usr/bin/env python
import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
import tf
import numpy as np
## END_SUB_TUTORIAL

from std_msgs.msg import String

def move_group_python_interface_tutorial():
  ## BEGIN_TUTORIAL
  ##
  ## Setup
  ## ^^^^^
  ## CALL_SUB_TUTORIAL imports
  ##
  ## First initialize moveit_commander and rospy.
  print "============ Starting tutorial setup"
  moveit_commander.roscpp_initialize(sys.argv)
  rospy.init_node('cart',
                  anonymous=True)

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
  
  ## Set velocity scaling factor
  #group.set_max_velocity_scaling_factor(0.05)	

  group.set_planner_id('RRTkConfigDefault')
  ## We create this DisplayTrajectory publisher which is used below to publish
  ## trajectories for RVIZ to visualize.
  display_trajectory_publisher = rospy.Publisher(
                                      '/move_group/display_planned_path',
                                      moveit_msgs.msg.DisplayTrajectory)

  

  listener = tf.TransformListener()
  rospy.sleep(5)
  (trans,rot) = listener.lookupTransform('world','kinect_link', rospy.Time(0))  

  print "Translational transformation from ee_link to world is:"
  print trans
  print "Rotational transformation ee_link to world is:"
  print rot
  transMatrix = listener.fromTranslationRotation(trans, rot)
  print "Transformation matrix is:"
  print transMatrix

  x_cam = 0.0
  y_cam = 0.0
  z_cam= -0.05
  #ee_matrix = np.matrix((1,0,0,x_ee),(0, 1, 0, y_ee),(0, 0, 1, z_ee),(0, 0, 0, 1)) 
  #doesn't need to be matrix -just vector?
  target_vector = np.array([x_cam, y_cam, z_cam, 1])
  world_target =  np.dot(transMatrix,target_vector)
  print "Transformed targets are:"
  print world_target
  ## Wait for RVIZ to initialize. This sleep is ONLY to allow Rviz to come up.
  print "============ Waiting for RVIZ..."
  rospy.sleep(10)
 

  print "Current ee_link Pose is:"
  print group.get_current_pose(end_effector_link = "ee_link")

  

  ## Cartesian Paths
  ## ^^^^^^^^^^^^^^^
  ## You can plan a cartesian path directly by specifying a list of waypoints 
  ## for the end-effector to go through.
  waypoints = []

  # start with the current pose
  waypoints.append(group.get_current_pose().pose)
 
  roll = -1.57;
  pitch = 0;
  yaw = 0;
  
  quaternion = tf.transformations.quaternion_from_euler(roll, pitch, yaw)

  # first orient gripper and move forward (+x)
  wpose = geometry_msgs.msg.Pose()
  wpose = group.get_current_pose().pose;
  
  euler = tf.transformations.euler_from_quaternion([wpose.orientation.x ,wpose.orientation.y,wpose.orientation.z,wpose.orientation.w])

  print "current orientation"
  print euler
  wpose.position.x = 0.826
  wpose.position.y = 0.1
  wpose.position.z = 1.5
  wpose.orientation.x = 0.0
  wpose.orientation.y = 0.0
  wpose.orientation.z = 0.016
  wpose.orientation.w = 1.0

  
  #wpose.orientation.x = quaternion[0]
  #wpose.orientation.y = quaternion[1]
  #wpose.orientation.z = quaternion[2]
  #wpose.orientation.w = quaternion[3]
  waypoints.append(copy.deepcopy(wpose))

  print "Desired ee_link Pose is:"
  print wpose

  group.clear_pose_targets()
  group.set_pose_target(wpose)

  ## We want the cartesian path to be interpolated at a resolution of 1 cm
  ## which is why we will specify 0.01 as the eef_step in cartesian
  ## translation.  We will specify the jump threshold as 0.0, effectively
  ## disabling it.
  #(plan3, fraction) = group.compute_cartesian_path(waypoints, 0.001,  0.0)         # jump_threshold
                               
  print "============ Waiting while RVIZ displays plan3..."
  rospy.sleep(5)

  #group.execute(plan3)
  group.go(wait=True)

  print "New ee_link Pose is:"
  print group.get_current_pose(end_effector_link = "ee_link")



  ## When finished shut down moveit_commander.
  moveit_commander.roscpp_shutdown()

  ## END_TUTORIAL

  print "============ STOPPING"

def addObstacles():
	scene = moveit_commander.PlanningSceneInterface()
	REFERENCE_FRAME = '/base_link'
	Platform_id = 'Platform'
	rospy.sleep(1)
	scene.remove_world_object(Platform_id) #what is this line for?
	pose_Platform = geometry_msgs.msg.PoseStamped()
	pose_Platform.header.frame_id = REFERENCE_FRAME
	pose_Platform.pose.position.x = 0.0 #edge co-ordinates, sides = half measured and height = 0 (i.e. at base link)
	pose_Platform.pose.position.y = 0.0
	pose_Platform.pose.position.z = -0.45
	scene.add_box(Platform_id,pose_Platform,(0.6,0.6,0.8))
	#test front obstacle
	Test_id = 'Test'
	rospy.sleep(1)
	scene.remove_world_object(Test_id) #what is this line for?
	pose_Test = geometry_msgs.msg.PoseStamped()
	pose_Test.header.frame_id = REFERENCE_FRAME
	pose_Test.pose.position.x = 0.5 #edge co-ordinates, sides = half measured and height = 0 (i.e. at base link)
	pose_Test.pose.position.y = 0.25
	pose_Test.pose.position.z = 0.5
	scene.add_box(Test_id,pose_Test,(0.2,0.4,0.8))

	rospy.sleep(1)

if __name__=='__main__':
  try:
    move_group_python_interface_tutorial()
    #addObstacles()
  except rospy.ROSInterruptException:
    pass


