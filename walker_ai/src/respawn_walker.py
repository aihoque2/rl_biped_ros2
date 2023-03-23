#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from gazebo_msgs.srv import SpawnEntity

class SpawnWalker(Node):
    def __init__(self, robot_description):
        super().__init__("spawn_walker_client")
        self.cli = self.create_client(SpawnEntity, "/spawn_entity")
        self.req = SpawnEntity.Request()
        self.req.name="bipedal_walker"
        
        #TODO: get the parameter robot_publisher from node /robot_state_publisher
