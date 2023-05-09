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

class SimpleSub(Node):
    
    def __init__(self):
        super().__init__("simple_sub")
        self.sub = self.create_subscription(String, 'ammar', self.listener_callback, 1)
    
    def listener_callback(self, msg):
        self.get_logger().info('I heard: "%s"' % msg.data)


if __name__ == '__main__':
    rclpy.init()

    simple_sub = SimpleSub()
    rclpy.spin(simple_sub)
    simple_sub.destroy_node()
    rclpy.shutdown()