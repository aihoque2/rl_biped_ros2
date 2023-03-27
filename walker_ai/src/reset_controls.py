#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from controller_manager_msgs.srv import SwitchController
from gazebo_msgs.srv import SpawnEntity, DeleteEntity
from geometry_msgs.msg import Pose

class ControllerResetClient(Node):
    def __init__(self):
        super().__init__("controller_reset")
        self.cli = self.create_client(SwitchController, "/controller_manager/switch_controller")
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("service not available, waiting again...")
        self.req = SwitchController.Request()
    
    def send_request(self, activate_controllers=[], deactivate_controllers=[]):
        self.req.activate_controllers = activate_controllers
        self.req.deactivate_controllers = deactivate_controllers
        self.req.activate_asap = True
        self.req.strictness=1 #BEST_EFFORT=1, STRICT=2
        self.future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()
    
    def activate_controls(self):
        result = False
        controller_arr = ["joint_effort_controller", "joint_state_broadcaster"]
        result = self.send_request(active_controllers=controller_arr)
        return result

    def reset_controls(self):
        #reset controls from deactivation to activation
        result = False
        controller_arr = ["joint_effort_controller", "joint_state_broadcaster"]
        deactivate_ok = self.send_request(activate_controllers=[], deactivate_controllers=controller_arr)
        if deactivate_ok:
            activate_ok = self.send_request(activate_controllers=controller_arr, deactivate_controllers=[])
            if activate_ok:
                self.get_logger().info("controllers reset!")
                result = True
            else:
                self.get_logger().info("activate ok ==> " + str(activate_ok))
        else:
            self.get_logger().info("DEactivate_ok ==> " + str(deactivate_ok))

        return result
    

if __name__ == "__main__":
    rclpy.init()
    reset_controls = ControllerResetClient()
    response = reset_controls.reset_controls()
    reset_controls.get_logger().info("controllers reset!")
    reset_controls.destroy_node()
    rclpy.shutdown()


