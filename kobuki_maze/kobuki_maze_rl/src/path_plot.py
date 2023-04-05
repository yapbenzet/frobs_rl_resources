#!/usr/bin/env python

import rospy
import matplotlib.pyplot as plt
from nav_msgs.msg import Odometry

path_x = []
path_y = []

def odom_callback(data):
    x = data.pose.pose.position.x
    y = data.pose.pose.position.y
    path_x.append(x)
    path_y.append(y)

rospy.init_node('path_plotter')
rospy.Subscriber('/odom', Odometry, odom_callback)

while not rospy.is_shutdown():
    rospy.spin()

plt.plot(path_x, path_y)
plt.title('Traveled Path')
plt.xlabel('X')
plt.ylabel('Y')
plt.show()