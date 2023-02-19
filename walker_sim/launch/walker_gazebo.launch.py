#!/usr/bin/python3
# -*- coding:   utf-8 -*-
import os

from ament_index_python.packages import get_package_share_directory, get_package_share_path
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


import xacro


def generate_launch_description():
    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')
    walker_sim_path = get_package_share_path('walker_sim')
    
    default_model_path = walker_sim_path / 'robots/simple_walker.urdf'
    print("ECHO: went thru default_model_path")
    model_arg = DeclareLaunchArgument(name='model', default_value=str(default_model_path), description="absolute path to robot urdf file")

    robot_description = ParameterValue(Command(['xacro ', LaunchConfiguration('model')]),
                                       value_type=str)
        
    print("ECHO: urdf parsed!")
    params =  {"robot_description": robot_description} #params for robot_state_publisher_node
    robot_state_publisher_node = Node(package = 'robot_state_publisher', 
                                      executable='robot_state_publisher', 
                                       parameters=[params],
                                      output='screen')

    # Gazebo launch
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gazebo.launch.py'),
        )
    )    

    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
                        arguments=['-topic', 'robot_description',
                                   '-entity', 'bipedal_walker'],
                        output='screen')

    return LaunchDescription([
        model_arg,
        robot_state_publisher_node,
        gazebo,
        spawn_entity
    ])