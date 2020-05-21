
# Pre-requsites

1) Install all Tb3 packages
2) sudo apt install ros-melodic-slam-gmapping

# Gmapping with Turtlebot3

## Launch the world and gmapping package

1) roslaunch pursuit_evasion robot_mapping.launch

## To drive autonomously with Turtlebot3 to map(not suggested)

2) roslaunch turtlebot3_gazebo turtlebot3_simulation.launch

## Using teleop to move around and create map

2) roslaunch turtlebot3_teleop turtlebot3_teleop_key.launch

## Saving the created map

3) rosrun map_server map_saver -f ~/map