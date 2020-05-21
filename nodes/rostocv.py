#!/usr/bin/env python

from __future__ import print_function

import roslib
roslib.load_manifest('turtle_description')
import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import numpy as np
import sys
sys.path.insert(0, '/home/malaynagda/darkflow')
import os
from darkflow.net.build import TFNet
import time
from geometry_msgs.msg import Pose, PoseWithCovarianceStamped, PoseStamped
from move_base_msgs.msg import MoveBaseActionResult, MoveBaseGoal
import actionlib
from actionlib_msgs.msg import *

print('_______________________________________',os.getcwd())
options = {"model": "/home/malaynagda/darkflow/cfg/yolo.cfg", "load": "/home/malaynagda/darkflow/cfg/yolo.weights", "threshold": 0.1,"config":"/home/malaynagda/darkflow/cfg/"}

tfnet = TFNet(options)
#/tb3_0/move_base/goal
class image_converter: 
	def __init__(self):
		#rospy.Timer(rospy.Duration(30), self.my_callback)
		#print('returned1')
		self.image_pub = rospy.Publisher("/tb3_0/tracking",Image) 
		self.bridge = CvBridge()
		self.image_sub = rospy.Subscriber("/tb3_0/rrbot/camera1/image_raw",Image,self.callback)

		self.bot_pose= rospy.Subscriber("/tb3_0/amcl_pose",PoseWithCovarianceStamped,self.update_initial_pose)
	def callback(self,data):
		try:
			cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
			#print("success")
		except CvBridgeError as e:
			print(e) 
		img=np.asarray(cv_image)
		results = tfnet.return_predict(img)			
		print('test',results)
    		newImage = np.copy(cv_image)
		results= results[0]
		
        	top_x = int(results['topleft']['x'])
        	top_y = int(results['topleft']['y'])

        	btm_x = int(results['bottomright']['x'])
        	btm_y = int(results['bottomright']['y'])

		c_x= float((top_x + btm_x)/2)
		c_y= float((top_y + btm_y)/2)
		w, h=btm_x- top_x, btm_y- top_y
		#print('w, h, c_x, cy__________________________________________________', w, h, c_x, c_y)
		
		if results['label']=='person':
		
			goal= PoseStamped()

			pub = rospy.Publisher('/tb3_0/move_base_simple/goal', PoseStamped, queue_size=100)	
			midpoint_bbox = float(c_x)
			#print(c_x)
			if 390 <= c_x <= 410:
				#print('1______________________________')
				goal.header.frame_id = "map"
				goal.pose.orientation.z = 0
				pub.publish(goal)
			elif c_x < 390:
				#print('2______________________________')
				goal.header.frame_id = "map"
				goal.pose.orientation.z = 1
				pub.publish(goal)

			elif c_x > 410:
				#print('3______________________________')
				goal.header.frame_id = "map"
				goal.pose.orientation.z = -1
				pub.publish(goal)

        	confidence = results['confidence']
        	label = results['label'] + " " + str(round(confidence, 3))
        	#if confidence > 0.05:
            		#newImage = cv2.rectangle(newImage, (top_x, top_y), (btm_x, btm_y), (255,0,0), 3)
            		#newImage = cv2.putText(newImage, label, (top_x, top_y-5), cv2.FONT_HERSHEY_COMPLEX_SMALL , 0.8, (0, 230, 0), 1, cv2.LINE_AA)
            	
			#cv2.imshow("Image window", newImage)
			#cv2.waitKey(500)
			#cv2.destroyAllWindows()
		try:
			self.image_pub.publish(self.bridge.cv2_to_imgmsg(cv_image, "bgr8"))
		except CvBridgeError as e:
			print(e)
	def update_initial_pose(self, initial_pose):
        	self.initial_pose = initial_pose
		print(initial_pose)
	def my_callback(event):
		print('over')
	

def main(args):
	print('returned1')
	ic = image_converter()
	print('returned2')
	rospy.init_node('image_converter', anonymous=True)
	try:
		rospy.spin()
	except KeyboardInterrupt:
		print("Shutting down") 

if __name__ == '__main__':
	main(sys.argv)

