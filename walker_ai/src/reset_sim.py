#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_srvs.srv import Empty
from std_msgs.msg import String

class ResetSimulation(Node):
    def __init__(self):
        super().__init__("simulation_reset_node")
        self.pub = self.create_publisher(String, 'ammar', 1)
        self.cli = self.create_client(Empty, '/reset_simulation')
        self.msg = String()
        self.msg.data = "simulation resetted!"
        timer_period = 0.5 # seconds
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("service not available, waiting again...")
        
        self.req = Empty.Request()

    def send_request(self):
        self.future = self.cli.call_async(self.req)
        #self.get_logger().info("published a reset: {}".format(self.msg.data))
        rclpy.spin_until_future_complete(self, self.future)
        self.pub.publish(self.msg)
        #rclpy.spin_once(self)
        #rclpy.spin_once(self.pub)
        return self.future.result()
    
if __name__ == "__main__":
    rclpy.init()
    reset_client = ResetSimulation()
    response = reset_client.send_request()
    reset_client.get_logger().info("Sim reset!")
    reset_client.destroy_node()
    rclpy.shutdown()
