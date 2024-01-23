#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import Image 
from cv_bridge import CvBridge, CvBridgeError 
import cv2
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
import rospy
import numpy as np

import moveit_commander
import time

class ColorFilter(object):

    def __init__(self):

        moveit_commander.roscpp_initialize([])
        self.robot = moveit_commander.RobotCommander()
        self.arm_group = moveit_commander.MoveGroupCommander("kuka_arm")
        self.gripper_group = moveit_commander.MoveGroupCommander("gripper")

        self.home_off = self.arm_group.get_named_target_values("home_off")
        self.lift_home = self.arm_group.get_named_target_values("lift_home")
        self.pick_conveyor = self.arm_group.get_named_target_values("pick_conveyor")
        self.lift_conveyor = self.arm_group.get_named_target_values("lift_conveyor")        
        self.place_green = self.arm_group.get_named_target_values("place_green")
        self.lift_green = self.arm_group.get_named_target_values("lift_green")
        self.place_blue = self.arm_group.get_named_target_values("place_blue")
        self.lift_blue = self.arm_group.get_named_target_values("lift_blue")
        self.place_red = self.arm_group.get_named_target_values("place_red")
        self.lift_red = self.arm_group.get_named_target_values("lift_red")        
        self.open_gripper = self.gripper_group.get_named_target_values("open_gripper")
        self.closed_gripper = self.gripper_group.get_named_target_values("closed_gripper")

        


    def run(self):   
        self.move_to_pose("home_off")
        time.sleep(0.60)
        self.move_to_pose("lift_home")
        time.sleep(0.60)
        self.move_to_pose("lift_conveyor")
        time.sleep(0.60)        
        self.move_to_pose("pick_conveyor")
        time.sleep(0.60)
        self.move_to_pose("lift_conveyor")
        time.sleep(0.60) 
        self.move_to_pose("lift_red")
        time.sleep(0.60) 
        self.move_to_pose("place_red")
        time.sleep(0.60) 
        self.move_to_pose("lift_red")
        time.sleep(0.60) 
        self.move_to_pose("lift_home")
        time.sleep(0.60) 
        

    def move_to_pose(self, pose_name):
        self.arm_group.set_named_target(pose_name)
        self.arm_group.go(wait=True)        

def main():
    color_filter_object = ColorFilter()
    rospy.init_node('color_filter_node', anonymous=True)
    color_filter_object.run()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print ("Shutting down")
    cv2.destroyAllWindows()


if __name__ == '__main__':
    print("Iniciando main")
    main()

