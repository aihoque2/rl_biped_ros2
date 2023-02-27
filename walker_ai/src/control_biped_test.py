import rclpy
from rclpy.node import Node

from std_msgs.msg import Float64MultiArray

class JointPub(Node):
    def __init__(self):
        super.__init__("joint_publisher")
        pass