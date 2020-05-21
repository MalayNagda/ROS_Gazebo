#!/usr/bin/env python
from __future__ import print_function

import roslib
roslib.load_manifest('turtle_description')
import sys
import rospy
from std_msgs.msg import Float64

def my_callback(event):
	print('Timer called at ', str(event.current_real))

def main(args):
	rospy.Timer(rospy.Duration(10), my_callback)

if __name__ == '__main__':
	rospy.init_node("timer")
	main(sys.argv)
