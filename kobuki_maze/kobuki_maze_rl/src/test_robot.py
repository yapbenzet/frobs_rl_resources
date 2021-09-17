#!/bin/python3

import gym
import rospy
import sys
from frobs_rl.common import ros_gazebo
from frobs_rl.common import ros_urdf
from frobs_rl.common import ros_spawn
from frobs_rl.common.ros_node import ROS_Kill_All_processes
from frobs_rl.wrappers.NormalizeActionWrapper import NormalizeActionWrapper
from frobs_rl.wrappers.TimeLimitWrapper import TimeLimitWrapper
from frobs_rl.wrappers.NormalizeObservWrapper import NormalizeObservWrapper

from kobuki_maze_rl.task_env import kobuki_maze

# Checker
from frobs_rl.models.utils import check_env

if __name__ == '__main__':


    # Launch Gazebo 
    ros_gazebo.Launch_Gazebo(paused=True,gui=True, pub_clock_frequency=100)

    # Start node
    rospy.logwarn("Start")
    rospy.init_node('kobuki_maze_test')

    # Launch env
    env = gym.make('KobukiMazeEnv-v0')

    # Check env
    check_env(env)