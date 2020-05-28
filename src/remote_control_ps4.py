#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Point

# LEFT JOYSTICK
BASE_HORIZONTAL = 0 
BASE_VERTICAL = 1

base_movement = Point()

def joy_data_callback(joy_data):
    base_movement.x = joy_data.axes[BASE_HORIZONTAL]
    base_movement.y = joy_data.axes[BASE_VERTICAL]
    


if __name__ == '__main__':
    try:
        rospy.init_node('andrewbot_rc_ps4', anonymous=True)
        rospy.Subscriber("joy", Joy,joy_data_callback)
        base_motion_pub = rospy.Publisher("andrewbot/BaseCommand", Point, queue_size=1)
        
        
        rate = rospy.Rate(100)  # 10ms
        while not rospy.is_shutdown():
            base_motion_pub.publish(base_movement)
        
            rate.sleep()
            

    except rospy.ROSInterruptException:
        rospy.loginfo("node terminated.")
    