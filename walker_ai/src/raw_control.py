#!/usr/bin/env python3
import rclpy
from rclpy import Node

from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint # Used for publishing mara joint angles.
from control_msgs.msg import JointTrajectoryControllerState

class RawControl(Node):
    def __init__(self):
        super().__init__("raw_control_node")
        self.joint_order = ['waist_thighR', 'thighR_shankR', 'waist_thighL', 'thighL_shankL']
        self.pub = self.create_publisher(JointTrajectory, "/walker/command")
        self.timer = self.create_timer()
    
    def timer_callback(self):
        pass