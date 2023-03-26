#!/usr/bin/env python3
import os
from ament_index_python.packages import get_package_share_directory

import rclpy
from rclpy.node import Node
from gazebo_msgs.srv import SpawnEntity


class SpawnWalker(Node):
    def __init__(self):
        super().__init__("spawn_walker_client")
        path = path = os.path.join(get_package_share_directory("walker_sim"), "robots", "simple_walker.urdf")
        self.cli = self.create_client(SpawnEntity, "/spawn_entity")
        self.urdf = open(path).read()
        self.req = SpawnEntity.Request()
        self.req.name="bipedal_walker"
        self.req.xml = self.urdf
    
    def send_request(self):
        future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, future)
        return future.result() # future is like promise in js?
        
if __name__ =="__main__":
    rclpy.init()
    respawn_node = SpawnWalker()
    response = respawn_node.send_request()
    respawn_node.get_logger().info("robot respawned!")
    respawn_node.destroy_node()
    rclpy.shutdown()
        