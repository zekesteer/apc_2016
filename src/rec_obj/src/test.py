#!/usr/bin/env python
from __future__ import print_function
import roslib
#roslib.load_manifest('../../package.xml')
import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError


class image_converter:

  def __init__(self):

    self.bridge = CvBridge()

    # Subscribe to the image topic that you want
    self.image_sub = rospy.Subscriber("/usb_cam/image_raw",Image,self.callback)

    cv2.namedWindow("Image from webcam", cv2.WINDOW_NORMAL)

  def callback(self,data):
    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
      print(e)

    (rows,cols,channels) = cv_image.shape
    if cols > 60 and rows > 60 :
      cv2.circle(cv_image, (50,50), 10, 255)

    cv2.imshow("Image from webcam", cv_image)
    cv2.waitKey(3)

    

def main(args):
  rospy.init_node('image_converter', anonymous=True)
  ic = image_converter()

  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")
  cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)