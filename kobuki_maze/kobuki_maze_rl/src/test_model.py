#!/bin/python3

from numpy.lib.npyio import save
from kobuki_maze_rl.task_env import kobuki_empty
from kobuki_maze_rl.task_env import kobuki_dynamic_v3
from kobuki_maze_rl.task_env import kobuki_maze
import gym
import rospy
import rospkg
import sys
from frobs_rl.common import ros_gazebo, ros_node
from frobs_rl.common.ros_node import ros_kill_all_processes
from frobs_rl.wrappers.NormalizeActionWrapper import NormalizeActionWrapper
from frobs_rl.wrappers.TimeLimitWrapper import TimeLimitWrapper
from frobs_rl.wrappers.NormalizeObservWrapper import NormalizeObservWrapper

# Models
from frobs_rl.models.td3 import TD3

if __name__ == '__main__':

    # Kill all processes related to previous runs
    ros_node.ros_kill_all_processes()

    # Launch Gazebo 
    ros_gazebo.launch_Gazebo(paused=True, gui=True)

    # Start node
    rospy.logwarn("Start")
    rospy.init_node('kobuki_maze_train')

    # Launch the task environment
    # env = gym.make('KobukiEmptyEnv-v0')
    # env = gym.make('KobukiDynamicEnv-v3')
    env = gym.make('KobukiMazeEnv-v0')

    #--- Normalize action space
    env = NormalizeActionWrapper(env)

    #--- Normalize observation space
    env = NormalizeObservWrapper(env)

    #--- Set max steps
    env = TimeLimitWrapper(env, max_steps=5000)
    env.reset()

    #--- Set the save and log path
    rospack = rospkg.RosPack()
    pkg_path = rospack.get_path("kobuki_maze_rl")

    
    #-- TD3
    # save_path = pkg_path + "/models/empty/td3/"
    # save_path = pkg_path + "/models/dynamic/td3/"
    save_path = pkg_path + "/models/maze/td3/"

    model = TD3.load_trained(save_path + "trained_model")

    obs = env.reset()
    episodes = 10
    epi_count = 0
    while epi_count < episodes:
        action, _states = model.predict(obs,deterministic=True)
        #action = env.action_space.sample()
        obs, _, dones, info = env.step(action)
        if dones:
            epi_count += 1
            rospy.logwarn("Episode: " + str(epi_count))
            obs = env.reset()

    env.close()
    sys.exit()