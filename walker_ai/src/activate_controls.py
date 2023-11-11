#!/usr/bin/env python3
#TODO: THIS ISNT EVEN STARTED YET. YOU JUST COPIED CODE WTF

import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_services_default


from controller_manager_msgs.srv import SwitchController
from builtin_interfaces.msg import Duration

class ControllerActivateClient(Node):
    def __init__(self):
        super().__init__("controller_reset")
        self.get_logger().info("creating client...")
        self.cli = self.create_client(SwitchController, "/controller_manager/switch_controller")
        while not self.cli.wait_for_service():
            self.get_logger().info("service not available, waiting again...")
        self.req = SwitchController.Request()
    
    def send_request(self, activate_controllers=[], deactivate_controllers=[]):
        self.req.activate_controllers = activate_controllers
        self.req.deactivate_controllers = deactivate_controllers
        self.req.activate_asap = True
        self.req.strictness=2 #BEST_EFFORT=1, STRICT=2
        self.req.timeout=Duration()
        self.req.timeout.sec=5

        self.future = self.cli.call(self.req)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()

    def activate_controls(self):
        # activate our controls with the client
        self.get_logger().info("resetting controls...")
    
        controller_arr = ["joint_effort_controller", "joint_state_broadcaster"]
        activate_ok = self.send_request(activate_controllers=controller_arr, deactivate_controllers=[])
    
        return True if activate_ok else False
    

if __name__ == "__main__":
    rclpy.init()
    activate_controls = ControllerActivateClient()
    activate_controls.get_logger().info("activate_controls client created!")
    response = activate_controls.activate_controls()
    activate_controls.get_logger().info("controllers activated!")
    activate_controls.get_logger().info("here's strictness: "+ str(activate_controls.req.strictness))
    activate_controls.destroy_node()
    rclpy.shutdown()


