# ROS_Gazebo
 A project showcasing perception in robotics with ROS, Gazebo simulaor and OpenCV. It involves simulation for navigation, SLAM, object detection and tracking using turtlebot3 ROS package.
 
## Overview
The entire project has three sections-
1. [Introduction to ROS](#1-introduction-to-ros)
2. [World building in Gazebo and robot interaction in it](#2-world-building-in-gazebo-and-robot-interaction-in-it)
3. [SLAM, object detection and tracking](#3-slam-object-detection-and-tracking)

## 1. Introduction to ROS
The purpose of this assignment was to get acquainted with the fundamentals of ROS- how to create a ROS workspace, packages, topics, nodes, messages, publishing and subscribing messages.

The objective was to write a node that makes the turtlesim write the first letter of my last name which is ‘N’. First, I created a workspace and package 'nodes' within that workspace and then made a node ‘my_initials_turtlesim.py’ in that package. This node can be seen in the similar folder structure above. 

### Code Explanation
To make the turtlesim move, we publish messages to the ROS topic cmd_vel. For the rostopic of cmd_vel, the message type is geometry_msgs/Twist which expects two vectors (one for linear velocity and the other for angular velocity) with three float64 values each for the three axes. I initialized them to zero values and published the same to the topic.
 
The letter ‘N’ is represented by three edges. First, I turn the turtle by a specific angle by passing the angle value by which I want to move the turtle, to the z component of angular velocity vector. Since angular velocity is directly proportional to the angle (with respect to a fixed point), I simply publish the desired angle in radians to the topic cmd_vel. After moving the turtle at a desired angle, I had to move the turtle forward by a particular distance for making the edges of the letter ‘N’. To ensure both the parallel edges of letter ‘N’ are of the same length, I passed the linear velocity of value 1 to the x component of linear velocity vector and kept on publishing it till the turtle had moved by the specified distance. I calculated the distance using ‘Distance= Speed x (Current time- Initial time)’.
 
After publishing each desired angular and linear velocity, the program waits for 3 seconds with the help of the command ‘time.sleep(3)’ to ensure the turtle has completed moving with the published desired velocity value. After this, I have published 0 value to the cmd_vel to make sure the turtle moves only with the velocity value specified in the next publish command. 

I published just the z component of angular velocity for making the turtle take a turn as I wanted it to simply rotate about the point (i.e. about the z-axis if we imagine it coming out of the computer screen) it was on and not move in any other direction. Also, for linear velocity I published only the x component as the turtle was supposed to move only in the direction ahead (and it will be the x component as we rotate only about z axis from initial pose of the turtle and for every turn taken after that, so the turtle is always on the axes). 

The desired linear velocity and angular velocity values were specified in arrays, one for each vector and published the elements of both the arrays alternatively, first an element of angular velocity array (ang_z) and then an element of linear velocity array (vel_x). The elements of vel_x array were treated as distances to be moved.

### How to run

<p align="center">
  <img src="images/turtlesim_letterN.PNG">
</p>

In order to get the output as seen above, run the following two lines, each in a separate terminal tab/window-

```
rosrun turtlesim turtlesim_node
rosrun turtle_description my_initials_turtlesim.py
```
## 2. World building in Gazebo and robot interaction in it
The purpose of this project was to understand and use ROS Gazebo simulator along with making a robot interact with that world. 

The objective was to make a Gazebo world with a Turtlebot3 robot in it and teleoperate the robot to move to make the shape of letter ‘N’ in the world space built.

The world which is a house-like structure was built with the help of the following Gazebo tutorials-
1.	Building a world- http://gazebosim.org/tutorials?tut=build_world&cat=build_world
2.	Building Editor- http://gazebosim.org/tutorials?tut=building_editor&cat=build_world

Some views of the house structure I built in Gazebo simulator are as seen below-

<p align="center">
  <img src="images/house1.png">
</p>
<p align="center">
  <img src="images/house2.png">
</p>
<p align="center">
  <img src="images/house3.png">
</p>
Steps implemented to make the world with house structure are-
1. A picture of a floorplan of consisting of 3 rooms was imported in the 2D view of the building editor. 
2. Using the wall option from the palette, the outline of the floorplan was traced over to generate a structure with the walls in the 3D view. 
3. Next, the doors and windows were added to the structure according to their placings in the 2D floorplan image along with two café tables as obstacles. 
4. Lastly, the walls material and colour were changed. 
5. We saved the created model of a house as a .sdf file in the turtle_gazebo package that was created for this project. 

The turtlebot3 robot supposed to be launched in the house world built is part of the turtlebot3 package which can be found at- https://github.com/ROBOTIS-GIT/turtlebot3. More details about the package can be found at- http://wiki.ros.org/turtlebot3. 
The ‘turtle_gazebo’ package created in this project consists of the world file in the worlds folder; the world file contains the house model that we created using building editor along with the default sun and the ground plane models. This world file was referenced in the launch file ‘turtle_world’ which was to be launched in an empty world. The launch file also contains a robot spawn method which uses a small python script called spawn model to make a service call request to the gaebo_ros ROS node (named simply "gazebo" in the rostopic namespace) to add a custom URDF into Gazebo which in our case is the turtlebot3 model with a camera attached to the ‘base_scan’ link of the turtlebot3 robot model. 
The camera is not attached by default to the turtlebot3. The code to add a camera to the turtlebot3 was added in the ‘turtlebot3_burger.urdf.xacro’ file. The code to capture images from the camera was added in the ‘turtlebot3_burger.gazebo.xacro’ file. Both of these xacro files are in the ‘turtlebot3_description’ package within the turtlebot3 package referenced above. The reference used for adding a camera and capturing images is- http://gazebosim.org/tutorials?tut=ros_gzplugins
For running the entire simulation, the launch file is executed which initiates the gazebo environment with the house and the turtlebot3 in it. Then we launch the rviz environment to see the view from the turtlebot3’s perspective. We run the node path.py in the turtle_description package. In the rviz environment we add a path.py node to the topic ‘Path’ to trace the trajectory of the turtlebot3 as it moved around the house and made the letter ‘N’ in the end. Lastly we run the node ‘my_initials.py’ so that turtlebot3 starts traversing around the house and the letter ‘N’.


## 3. SLAM, object detection and tracking
