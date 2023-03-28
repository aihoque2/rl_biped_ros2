#include "rclcpp/rclcpp.hpp"
#include "controller_manager_msgs/srv/switch_controller.hpp"

#include <memory>
#include <string>
#include <vector>

using namespace std::chrono_literals;


std::vector<std::string> controller_arr = {"joint_effort_controller", "joint_state_broadcaster"};

class ControllerResetClient : public rclcpp::Node{
    public:
        //member vars
        rclcpp::Client<controller_manager_msgs::srv::SwitchController>::SharedPtr cli;
        std::shared_ptr<controller_manager_msgs::srv::SwitchController::Request> request;

        ControllerResetClient() : Node("controller_reset_cpp"){
            cli = this->create_client<controller_manager_msgs::srv::SwitchController>("/controller_manager/switch_controller");
            while (!cli->wait_for_service(1s)) {
                if (!rclcpp::ok()) {
                    RCLCPP_ERROR(this->get_logger(), "Interrupted while waiting for the service. Exiting.");
                }
                RCLCPP_INFO(this->get_logger(), "service not available, waiting again...");
            }
            request = std::make_shared<controller_manager_msgs::srv::SwitchController::Request>();
        }
        bool send_request(std::vector<std::string> activate_controllers, std::vector<std::string> deactivate_controllers){
            request->activate_controllers = activate_controllers;
            request->deactivate_controllers = deactivate_controllers;
            auto future = cli->async_send_request(request);
            if (rclcpp::spin_until_future_complete(this->get_node_base_interface(), future) == rclcpp::FutureReturnCode::SUCCESS) return true;
            else return false;
        }

        bool reset_controls(){
            RCLCPP_INFO(this->get_logger(), "restetting controls");
            bool result = false;
            bool deactivateOk = send_request({}, controller_arr);
            if (deactivateOk){
                bool activateOk = send_request(controller_arr, {});
                if (activateOk){
                    result = true;
                    RCLCPP_INFO(this->get_logger(), "activate successful!");
                }
                else RCLCPP_INFO(this->get_logger(), "activate failed");
            }
            else{
                RCLCPP_INFO(this->get_logger(), "ERROR: deactivate_ok is False!");
            }
            return result;
        }
};

int main(int argc, char * argv[])
{
    rclcpp::init(argc, argv);
    std::shared_ptr<ControllerResetClient> node = std::make_shared<ControllerResetClient>();
    rclcpp::shutdown();
    return 0;
}
