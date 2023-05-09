#!/usr/bin/env python3
import os
from ament_index_python.packages import get_package_share_directory

import rclpy
from rclpy.node import Node
from gazebo_msgs.srv import SpawnEntity
f
from spawn_entity import SpawnEntityNode

if __name__ =="__main__":
    rclpy.init()
    respawn_node = SpawnWalker()
    response = respawn_node.spawn_walker()
    respawn_node.get_logger().info("robot respawned!")
    respawn_node.destroy_node()
    rclpy.shutdown()
        