#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from std_msgs.msg import Float64MultiArray
from array import array

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
    rclpy.spin(joint_publisher)
    joint_publisher.position = "pos1"
    rclpy.spin_once(joint_publisher)
    joint_publisher.destroy_node()
    rclpy.shutdown()