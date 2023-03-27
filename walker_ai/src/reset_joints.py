#!/usr/bin/env python3
"""
reset_joints.py

reset joints node
"""
from array import array

import rclpy
from rclpy.node import Node

from std_msgs.msg import Float64MultiArray

class JointPub(Node):
    
    def __init__(self):
        super().__init__("joint_reset")
        self.pub = self.create_publisher(Float64MultiArray, "joint_effort_controller/commands", 10)
        self.pos = [0.0, 0.0, 0.0, 0.0]
        
        timer_period = 0.5
        self.timer = self.create_timer(timer_period, self.timer_callback)
    
    def timer_callback(self):
        msg = Float64MultiArray()
        msg.data = array('d', self.pos)
        self.pub.publish(msg)


if __name__ == '__main__':
    rclpy.init()

    joint_publisher = JointPub()
    rclpy.spin_once(joint_publisher)
    joint_publisher.destroy_node()
    joint_publisher.get_logger().info("joints reset!")
    rclpy.shutdown()