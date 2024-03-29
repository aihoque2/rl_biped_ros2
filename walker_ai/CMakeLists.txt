cmake_minimum_required(VERSION 3.5)
project(walker_ai)

# Default to C99
if(NOT CMAKE_C_STANDARD)
  set(CMAKE_C_STANDARD 99)
endif()

# Default to C++14
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(rclcpp REQUIRED)
find_package(controller_manager_msgs REQUIRED)
find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(control_msgs REQUIRED)
find_package(std_msgs REQUIRED)
find_package(gazebo_ros REQUIRED)
# uncomment the following section in order to fill in
# further dependencies manually.
# find_package(<dependency> REQUIRED)

add_executable(reset_controls_cpp src/reset_controls.cpp)
ament_target_dependencies(reset_controls_cpp rclcpp controller_manager_msgs)

add_executable(control_biped_cpp src/control_biped.cpp)
ament_target_dependencies(control_biped_cpp rclcpp std_msgs)

install(
  DIRECTORY src launch 
  DESTINATION share/${PROJECT_NAME}
)

# C++ install
install(TARGETS
  reset_controls_cpp
  control_biped_cpp
  DESTINATION lib/${PROJECT_NAME}
)

# ament_python_install_package(${PROJECT_NAME})
# python install
install(PROGRAMS
  src/control_biped_test_node.py
  src/reset_controls.py
  src/deactivate_controls.py
  src/activate_controls.py
  src/delete_walker.py
  src/reset_sim.py
  src/reset_joints.py
  src/simple_pub.py
  src/simple_sub.py
  DESTINATION lib/${PROJECT_NAME}
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # uncomment the line when a copyright and license is not present in all source files
  #set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # uncomment the line when this package is not in a git repo
  #set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
