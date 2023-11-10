#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_services_default


from controller_manager_msgs.srv import SwitchController
from builtin_interfaces.msg import Duration

class ControllerDeactivateClient(Node):
    def __init__(self):
        super().__init__("deactivate_controller")
        self.get_logger().info("creating client...")
        self.cli = self.create_client(SwitchController, "/controller_manager/switch_controller")
        while not self.cli.wait_for_service():
            self.get_logger().info("service not available, waiting again...")
        self.req = SwitchController.Request()
    
    def send_request(self, activate_controllers=[], deactivate_controllers=[]):
        self.req.activate_controllers = activate_controllers
        self.req.deactivate_controllers = deactivate_controllers
        self.req.activate_asap = True
        self.req.strictness=2 # BEST_EFFORT=1, STRICT=2
        self.req.timeout=Duration()
        self.req.timeout.nanosec = 10

        self.future = self.cli.call(self.req)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()

    def deactivate_controls(self):
        # deactivate controls with the client
        self.get_logger().info("deactivating controls...")

        controller_arr = ["joint_effort_controller", "joint_state_broadcaster"]
        deactivate_ok = self.send_request(activate_controllers=[], deactivate_controllers=controller_arr)
        return True if deactivate_ok else False # unsure of deactivate_ok's type
    

if __name__ == "__main__":
    rclpy.init()
    deatctivate_controls = ControllerDeactivateClient()
    deatctivate_controls.get_logger().info("deactivate_controls client created!")
    response = deatctivate_controls.deactivate_controls()
    deatctivate_controls.get_logger().info("controllers deactivated!")
    deatctivate_controls.get_logger().info("here's strictness: "+str(deatctivate_controls.req.strictness))
    deatctivate_controls.destroy_node()
    rclpy.shutdown()


