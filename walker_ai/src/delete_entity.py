import rclpy
from rclpy.node import Node
from gazebo_msgs.srv import DeleteEntity, SpawnEntity

class DeleteWalker(Node):
    def __init__(self):
        super().__init__("Delete Walker client")
        