#!/usr/bin/env python3
import os
from ament_index_python.packages import get_package_share_directory
import xml.etree.ElementTree as ET

import rclpy
from rclpy.node import Node
from gazebo_msgs.srv import SpawnEntity

contents = open("simple_walker.urdf").read()
print(contents)

class SpawnWalker(Node):
    def __init__(self, robot_description):
        super().__init__("spawn_walker_client")
        self.cli = self.create_client(SpawnEntity, "/spawn_entity")
        self.urdf = os.path.join
        self.req = SpawnEntity.Request()
        self.req.name="bipedal_walker"
        self.urdf = robot_description
        
        #TODO: get the parameter robot_publisher from node /robot_state_publisher

if __name__ =="__main":
    #contents = open("simple_walker.urdf").read() #TODO: RELATIVE PATHS? get_package_share_directory?
    #print(contents)
    pass
