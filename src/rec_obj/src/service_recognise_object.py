#!/usr/bin/python2.7

from __future__ import print_function
import roslib
#roslib.load_manifest('../../package.xml')
import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import apc_2016.srv
import threading
import detectObjects



def synchronized(method):

    lock = threading.Lock()
    
    def new_method(self, *arg, **kws):
        with lock:
            return method(self, *arg, **kws)

    return new_method



class image_converter:

  def __init__(self):

    self.bridge = CvBridge()
    self.image = None

    # Subscribe to the image topic that you want
    self.image_sub = rospy.Subscriber("/usb_cam/image_raw",Image,self.callback)

    self.image_pub = rospy.Publisher("image_from_object_recognition",Image)


  def callback(self,data):
    try:
      self.setImage(self.bridge.imgmsg_to_cv2(data, "bgr8"))
    except CvBridgeError as e:
      print(e)


  @synchronized
  def setImage(self, im):
    self.image = im

  @synchronized
  def getImage(self):
    return self.image


  def processImage(self, objectNames):

    while self.getImage() == None:
        continue

    self.image_sub.unregister()

    try:
        self.image_pub.publish(self.bridge.cv2_to_imgmsg(self.image, "bgr8"))
    except CvBridgeError as e:
        print(e)

#    cv2.namedWindow("Image from webcam", cv2.WINDOW_NORMAL)
#    cv2.imshow("Image from webcam", self.image)
#    cv2.waitKey(300)
#    
    #print("Before matching")
    
    name_matched_image_sift_global, kp_matched_image_sift_global, kpDest_sift, matches_sift_global_goodPoints, matches_sift_global_name, error_sift_global, M_sift_global, mask_sift_global = detectObjects.matchImageWithDatabase(self.image, "./keypoints/", "./poses/", ".png", objectNames)


#    cv2.destroyWindow("Image from webcam")
    #print("After matching")

    #print(name_matched_image_sift_global)

    if name_matched_image_sift_global != []:
        return name_matched_image_sift_global[0][:-2]
    else:
        return ""




# Function to recognise object
def handle_recognise_object(req):

    rospy.loginfo("list of objects: " + req.tote_obj_ids)

    listObjects = req.tote_obj_ids.split(',')

    im = image_converter()
    objectName = im.processImage(listObjects)

    return objectName




def server():

    # Initialisation of the service node
    rospy.init_node('rec_obj_srv_node')

    # Initialisation of the service
    s = rospy.Service('rec_obj_srv', apc_2016.srv.RecObjSrv, handle_recognise_object)

    rospy.spin()



if __name__ == "__main__":
    server()
