#!/usr/bin/env python3
"""
This is an example script.

It seems that it has to have THIS docstring with a summary line, a blank line
and sume more text like here. Wow.
"""
from array import array

import rclpy
from rclpy.node import Node

from std_msgs.msg import Float64MultiArray

class JointPub(Node):
    
    def __init__(self):
        super().__init__("joint_publisher")
        self.pub = self.create_publisher(Float64MultiArray, "joint_effort_controller/commands", 10)
        self.pos1 = [1.57, -1.57, 1.57, -1.57]
        self.pos2 = [0.0, 0.0, 0.0, 0.0]
        self.position = "pos1"
        
        timer_period = 0.5
        self.timer = self.create_timer(timer_period, self.timer_callback)
    
    def timer_callback(self):
        msg = Float64MultiArray()
        if self.position == "pos1":
            msg.data = array('d', self.pos1)
            self.pub.publish(msg)
            self.position = "pos2"
        else:
            msg.data = array('d', self.pos2)
            self.pub.publish(msg)
            self.position="pos1"


if __name__ == '__main__':
    rclpy.init()

    joint_publisher = JointPub()
    i = 0
    while (i < 10):
        rclpy.spin_once(joint_publisher)
        i+=1
    joint_publisher.position = "pos2"
    rclpy.spin_once(joint_publisher)
    joint_publisher.destroy_node()
    
    rclpy.shutdown()