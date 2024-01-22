#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import Image 
from cv_bridge import CvBridge, CvBridgeError 
import cv2
import numpy as np
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

class ColorBasedController(object):

    def __init__(self):
        self.image_sub = rospy.Subscriber("/camera1/color/image_raw", Image, self.camera_callback)
        self.trajectory_publisher = rospy.Publisher('/arm_controller/command', JointTrajectory, queue_size=10)
        self.bridge_object = CvBridge()
        
    def camera_callback(self, data):
        try:
            cv_image = self.bridge_object.imgmsg_to_cv2(data, desired_encoding="bgr8")
        except CvBridgeError as e:
            print(e)

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
        detected_color = ""
        if np.sum(mask_g) > np.sum(mask_r) and np.sum(mask_g) > np.sum(mask_b):
            detected_color = "verde"
        elif np.sum(mask_r) > np.sum(mask_g) and np.sum(mask_r) > np.sum(mask_b):
            detected_color = "rojo"
        elif np.sum(mask_b) > np.sum(mask_g) and np.sum(mask_b) > np.sum(mask_r):
            detected_color = "azul"

        print("La caja es de color " + detected_color)

        # Perform trajectory based on detected color
        self.perform_trajectory(detected_color)

    def perform_trajectory(self, detected_color):
        rospy.loginfo(f"Detected color: {detected_color}")

        # Define trajectory for each color
        if detected_color == "verde":
            goal_positions = [0, -0.5, 0.5, 0, 1.5, 0]
        elif detected_color == "rojo":
            goal_positions = [0, -0.5, 1, 0, 1, 0]
        elif detected_color == "azul":
            goal_positions = [0, -0.5, 2, 0, 2.5, 0]
        else:
            rospy.logwarn("Unknown color. No movement performed.")
            return

        # Create and publish JointTrajectory
        trajectory_msg = JointTrajectory()
        trajectory_msg.joint_names = ['joint_a1', 'joint_a2', 'joint_a3', 'joint_a4', 'joint_a5', 'joint_a6']
        trajectory_msg.points.append(JointTrajectoryPoint(positions=goal_positions, time_from_start=rospy.Duration(3)))

        self.trajectory_publisher.publish(trajectory_msg)

def main():
    color_based_controller = ColorBasedController()
    rospy.init_node('color_based_controller_node', anonymous=True)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")

if __name__ == '__main__':
    main()