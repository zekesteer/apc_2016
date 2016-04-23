#!/usr/bin/python2.7

import sys
import rospy
from amazon_object_recognition.srv import recognise_object

def test_client():

    rospy.wait_for_service('recognise_object')
    try:

		while True:

		    recognise = rospy.ServiceProxy('recognise_object', recognise_object)
		    resp1 = recognise()

#		    print resp1.code

		    if resp1.objectName != None:
		        print "OBJECT RECOGNISED:", resp1.objectName
		    else:
		        print "OBJECT RECOGNISED:"

			raw_input()


    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

if __name__ == "__main__":
	test_client()
