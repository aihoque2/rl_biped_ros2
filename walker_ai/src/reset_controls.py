#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_services_default

from controller_manager_msgs.srv import SwitchController
from gazebo_msgs.srv import SpawnEntity, DeleteEntity
from geometry_msgs.msg import Pose
from builtin_interfaces.msg import Duration

class ControllerResetClient(Node):
    def __init__(self):
        super().__init__("controller_reset")
        self.get_logger().info("creating client...")
        self.cli = self.create_client(SwitchController, "/controller_manager/switch_controller", qos_profile=qos_profile_services_default)
        while not self.cli.wait_for_service():
            self.get_logger().info("service not available, waiting again...")
        self.req = SwitchController.Request()
    
    def send_request(self, activate_controllers=[], deactivate_controllers=[]):
        self.req.activate_controllers = activate_controllers
        self.req.deactivate_controllers = deactivate_controllers
        self.req.activate_asap = True
        self.req.strictness=2 #BEST_EFFORT=1, STRICT=2
        self.future = self.cli.call_async(self.req)
        self.req.timeout=Duration()
        self.req.timeout.sec = 10
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()

    def reset_controls(self):
        #reset controls from deactivation to activation
        self.get_logger().info("resetting controls...")
        result = False
        controller_arr = ["joint_effort_controller", "joint_state_broadcaster"]
        deactivate_ok = self.send_request(activate_controllers=[], deactivate_controllers=controller_arr)
        if deactivate_ok:
            self.get_logger().info("deactivated the controller")
            activate_ok = self.send_request(activate_controllers=controller_arr, deactivate_controllers=[])
            if activate_ok:
                self.get_logger().info("controllers reset!")
                result = True
            else:
                self.get_logger().info("activate_ok ==> " + str(activate_ok))
        else:
            self.get_logger().info("DEactivate_ok ==> " + str(deactivate_ok))

        return result
    

if __name__ == "__main__":
    rclpy.init()
    reset_controls = ControllerResetClient()
    reset_controls.get_logger().info("client created!")
    response = reset_controls.reset_controls()
    reset_controls.get_logger().info("controllers reset!")
    reset_controls.get_logger().info("here's strictness: "+str(reset_controls.req.strictness))
    reset_controls.destroy_node()
    rclpy.shutdown()


