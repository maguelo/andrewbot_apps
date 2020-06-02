#!/usr/bin/env python
import rospy
import math
from sensor_msgs.msg import Joy

from geometry_msgs.msg import Twist
from andrewbot_utils.math_utils import translate_point_to_twist



# LEFT JOYSTICK
BASE_HORIZONTAL = 0 
BASE_VERTICAL = 1

base_movement = Twist()

base_motion_pub = rospy.Publisher("andrewbot/BaseCommand", Twist, queue_size=1)
# To test with turtlesim
#base_motion_pub = rospy.Publisher("/turtle1/cmd_vel", Twist, queue_size=1)


def move_base(joy_data):
    x = -joy_data.axes[BASE_HORIZONTAL]
    y = joy_data.axes[BASE_VERTICAL]

    base_movement.linear.x, base_movement.angular.z = translate_point_to_twist(x, y)



# RIGHT JOYSTICK
HEAD_HORIZONTAL = 3
HEAD_VERTICAL = 4

head_movement = Twist()
head_motion_pub = rospy.Publisher("andrewbot/HeadCommand", Twist, queue_size=1)

def move_head(joy_data):
    head_movement.angular.x = -joy_data.axes[HEAD_HORIZONTAL]
    head_movement.angular.z =  joy_data.axes[HEAD_VERTICAL]


def joy_data_callback(joy_data):
    move_base(joy_data)
    move_head(joy_data)
    
    

import time
if __name__ == '__main__':
    try:
        rospy.init_node('andrewbot_rc_ps4', anonymous=True)
        rospy.Subscriber("joy", Joy,joy_data_callback)
        
        
        
        rate = rospy.Rate(100)  # 10ms    100
        while not rospy.is_shutdown():
            base_motion_pub.publish(base_movement)
            head_motion_pub.publish(head_movement)
            rate.sleep()
            
    except rospy.ROSInterruptException:
        rospy.loginfo("node terminated.")
    