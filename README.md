This project was built taking ROS Noetic into consideration. Execution on ROS Melodic may be compatible, but not recomended.

If cloned or downloaded, please delete devel and build folders, as well as CMakeList.txt on /catkin_ws/src.

Commands required:

sudo apt-get update 
source /opt/ros/$ROS_DISTRO/setup.bash 
sudo apt-get install ros-noetic-joint-state-controller 
sudo apt-get install ros-noetic-effort-controllers 
sudo apt-get install ros-noetic-position-controllers 
sudo apt install ros-noetic-industrial-core
sudo apt-get install ros-noetic-object-recognition-msgs 

Repositories needed:

git clone https://github.com/javierpagalo/Gazebo_utils.git

git clone https://github.com/roboticsgroup/roboticsgroup_upatras_gazebo_plugins.git

We STRONGLY recommend unzipping the Robotiq-grippers.zip file instead of clonning the repository, but both are provided:
git clone https://github.com/fryumbla/Robotiq-grippers.git

Install dependencies needed:

rosdep install --from-paths src --ignore-src -r -y

Build project:

catkin_make

To execute, you must run the following code:

cd catkin_ws
source devel/setup.bash
roslaunch kr150_gazebo kr150_gazebo.launch

Each line in another terminal with the same directory (please execute "source devel/setup.bash" on each terminal):
roslaunch kuka_arm_2f_moveit move_group.launch
rosrun kr150_master color_sensorV2.py
rosrun kr150_master box_spawner.py
