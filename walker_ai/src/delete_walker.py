#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from gazebo_msgs.srv import DeleteEntity

class DeleteWalker(Node):
    """
    client node
    """
    def __init__(self):
        super().__init__("delete_walker_client")
        self.cli = self.create_client(DeleteEntity,"/delete_entity")
        self.req = DeleteEntity.Request()
        self.req.name = "bipedal_walker" # TODO: where did you get this name?

        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("service not available, waiting again...")
        
        self.req.name  = "bipedal_walker"

    def send_request(self):
        future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, future)
        return future.result()
    
if __name__ == "__main__":
    rclpy.init()
    delete_client = DeleteWalker()
    response = delete_client.send_request()
    delete_client.get_logger().info("entity deleted!")
    delete_client.destroy_node()
    rclpy.shutdown()
