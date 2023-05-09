#!/usr/bin/env python3
"""
This is an example script.

It seems that it has to have THIS docstring with a summary line, a blank line
and sume more text like here. Wow.
"""
from array import array

import rclpy
from rclpy.node import Node

from std_msgs.msg import String

class SimplePub(Node):
    
    def __init__(self):
        super().__init__("simple_pub")
        self.pub = self.create_publisher(String, "ammar", 10)

        self.msg = String()
        self.msg.data = "yeet"
        
        timer_period = 0.5
        self.timer = self.create_timer(timer_period, self.timer_callback)
    
    def timer_callback(self):
        self.pub.publish(self.msg)


if __name__ == '__main__':
    rclpy.init()

    simple_pub = SimplePub()
    i = 0
    while (i < 10):
        rclpy.spin_once(simple_pub)
        i+=1
    simple_pub.destroy_node()
    rclpy.shutdown()