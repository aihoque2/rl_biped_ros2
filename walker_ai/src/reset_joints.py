#!/usr/bin/env python3
"""
reset_joints.py

reset joints node
"""
from array import array

import rclpy
from rclpy.node import Node

from std_msgs.msg import Float64MultiArray
from std_srvs.srv import Empty
from controller_manager_msgs.srv import SwitchController

class JointPub(Node):
    
    def __init__(self):
        super().__init__("joint_reset")
        
        # self.sim_cli = self.create_client(Empty, "/reset_sim")
        # while not self.cli.wait_for_service(timeout_sec=1.0):
        #     self.get_logger().info("service not available, waiting again...")
        # self.sim_req = Empty.Request()

        # self.control_cli = self.create_client(SwitchController, "/controller_manager/switch_controller")
        # while not self.cli.wait_for_service():
        #     self.get_logger().info("service not available, waiting again...")
        # self.control_req = SwitchController.Request()

        self.pub = self.create_publisher(Float64MultiArray, "joint_effort_controller/commands", 10)
        self.pos = [0.0, 0.0, 0.0, 0.0]
        
        timer_period = 0.25
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