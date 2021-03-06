#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
import time
					
if __name__ == '__main__':

	rospy.init_node('my_initials_turtlesim', anonymous= True)
	vel_pub= rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
	velocity=Twist()

	length=15.0
	velocity.linear.x=0.0
	velocity.linear.y=0.0
	velocity.linear.z=0.0
	velocity.angular.x=0.0
	velocity.angular.y=0.0
	velocity.angular.z=0.0

	time.sleep(2)
	vel_pub.publish(velocity)     #Ensuring turtle starts from 0 linear & angular velocity
	time.sleep(2)

	vel_x=[3,4.5,3]               #Linear speed for each edge of letter
	ang_z=[1.5707,-2.35619,2.618] #Angle between two edges 
	
	for i in range(len(ang_z)):

		time.sleep(3)
		velocity.angular.z=ang_z[i]
		vel_pub.publish(velocity)
		time.sleep(3)
		
		velocity.angular.z=0.0
		time.sleep(3)
		t0 = rospy.Time.now().to_sec()
		current_distance = 0
		while(current_distance < vel_x[i]):

			velocity.linear.x= 1
			t1=rospy.Time.now().to_sec()
			current_distance= (t1-t0)
			vel_pub.publish(velocity)
		time.sleep(3)
		print('Step %d',i)

		velocity.linear.x=0.0
		time.sleep(3)

