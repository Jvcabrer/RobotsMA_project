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

        self.image_sub = rospy.Subscriber("/camera1/color/image_raw", Image, self.camera_callback)
        self.bridge_object = CvBridge()
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

        self.detected_color = None
        
    def camera_callback(self, data):
        try:
            # We select bgr8 because its the OpenCV encoding by default
            cv_image = self.bridge_object.imgmsg_to_cv2(
                data, desired_encoding="bgr8")
        except CvBridgeError as e:
            print (e)

        #image = cv2. imread (example_path)
        # I resized the image so it can be easier to work with
        image = cv2.resize(cv_image, (300, 300))

        # Once we read the image we need to change the color space to HSV
        hsv = cv2.cvtColor (image, cv2.COLOR_BGR2HSV)

        # Hsv limits are defined
        # here is where you define the range of the color you are looking for
        # each value of the vector corresponds to the H,S & V values respectively
        min_green = np.array([40, 50, 50])
        max_green = np.array([60, 255, 255])

        min_red = np.array ([0, 45, 142])
        max_red = np.array ([10, 255, 255])

        min_blue = np.array ([100, 50, 50])
        max_blue = np.array([120, 255, 255])

        # This is the actual color detection
        # Here we will create a mask that contains only the colors defined in your limits
        # This mask has only one dimention, so its black and white }
        mask_g = cv2.inRange(hsv, min_green, max_green)
        mask_r = cv2.inRange(hsv, min_red, max_red)
        mask_b = cv2.inRange(hsv, min_blue, max_blue)

        # We use the mask with the original image to get the colored post-processed image
        res_b = cv2.bitwise_and(image, image, mask=mask_b)
        res_g = cv2.bitwise_and(image, image, mask=mask_g)
        res_r = cv2.bitwise_and(image, image, mask=mask_r)

        cv2.imshow('Original',image)
        cv2.imshow('Green',res_g)
        cv2.imshow('Red',res_r)
        cv2.imshow('Blue',res_b)
        cv2.waitKey(1)

        # Determine the detected color
        self.detected_color = ""
        if np.sum(mask_g) > np.sum(mask_r) and np.sum(mask_g) > np.sum(mask_b):
            self.detected_color = "green"
        elif np.sum(mask_r) > np.sum(mask_g) and np.sum(mask_r) > np.sum(mask_b):
            self.detected_color = "red"
            print("pick n place red")
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
        elif np.sum(mask_b) > np.sum(mask_g) and np.sum(mask_b) > np.sum(mask_r):
            self.detected_color = "blue"
        else:
            self.detected_color = "none"   
            self.move_to_pose("lift_home")
            time.sleep(0.60)
        #print("Detected color " + self.detected_color)


    def run(self):
        if self.detected_color == "red":
            print("pick n place red")
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
        elif self.detected_color == "green":
            print("pick n place green")
            self.move_to_pose("lift_home")
            time.sleep(0.60)
            self.move_to_pose("lift_conveyor")
            time.sleep(0.60)        
            self.move_to_pose("pick_conveyor")
            time.sleep(0.60)
            self.move_to_pose("lift_conveyor")
            time.sleep(0.60) 
            self.move_to_pose("lift_green")
            time.sleep(0.60) 
            self.move_to_pose("place_green")
            time.sleep(0.60) 
            self.move_to_pose("lift_green")
            time.sleep(0.60) 
            self.move_to_pose("lift_home")
            time.sleep(0.60) 
        elif self.detected_color == "blue":
            print("pick n place blue")
            self.move_to_pose("lift_home")
            time.sleep(0.60)
            self.move_to_pose("lift_conveyor")
            time.sleep(0.60)        
            self.move_to_pose("pick_conveyor")
            time.sleep(0.60)
            self.move_to_pose("lift_conveyor")
            time.sleep(0.60) 
            self.move_to_pose("lift_blue")
            time.sleep(0.60) 
            self.move_to_pose("place_blue")
            time.sleep(0.60) 
            self.move_to_pose("lift_blue")
            time.sleep(0.60) 
            self.move_to_pose("lift_home")
            time.sleep(0.60) 

            
    def move_to_pose(self, pose_name):
        self.arm_group.set_named_target(pose_name)
        self.arm_group.go(wait=True)  


def main():
    color_filter_object = ColorFilter()
    rospy.init_node('color_filter_object', anonymous=True)
    color_filter_object.run()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print ("Shutting down")
    cv2.destroyAllWindows()


if __name__ == '__main__':
    print("Iniciando main")
    main()

