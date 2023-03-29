#!/usr/bin/env python3
import rclpy
"""
raw_control.py

ros2_control, and gazebo_ros2 SUCK
this is my attempt to experiment 
with controls using barebones ROS 
"""

from rclpy import Node

from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint # Used for publishing hip and knee joint angles
from control_msgs.msg import JointTrajectoryControllerState

class RawControl(Node):
    def __init__(self):
        super().__init__("raw_control_node")
        self.joint_order = ['waist_thighR', 'thighR_shankR', 'waist_thighL', 'thighL_shankL']
        self.pub = self.create_publisher(JointTrajectory, "/bipedal_controller/command")
        self.pos1 = [1.57, -1.57, 1.57, -1.57]
        self.pos2 = [0.0, 0.0, 0.0, 0.0]
        self.position = "pos1"
        
        timer_period = 0.5
        self.timer = self.create_timer(timer_period, self.timer_callback)
    
    def timer_callback(self):
        pass