#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_srvs.srv import Empty

class ResetSimulation(Node):
    def __init__(self):
        super().__init__("simulation_reset_node")
        self.cli = self.create_client(Empty, '/reset_simulation')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("service not available, waiting again...")
        
        self.req = Empty.Request()

    def send_request(self):
        self.future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()
    
if __name__ == "__main__":
    rclpy.init()
    reset_client = ResetSimulation()
    response = reset_client.send_request()
    reset_client.get_logger().info("Sim reset!")
    reset_client.destroy_node()
    rclpy.shutdown()
