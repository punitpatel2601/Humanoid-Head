#!/usr/bin/env python3

# imports
from numpy import rate
import rospy
from std_msgs.msg import Bool


# simulates the turning on and off of led on Robot
def update_light(recieved):
    rospy.loginfo("Updating light lumens: ")
    rospy.loginfo(recieved.data)


def warning_led_sim():
    # subscribe and listen the data from gas monitoring service
    rospy.init_node('Light', anonymous=True)

    rospy.Subscriber('Update_Light_Lumens', Bool, update_light)



if __name__ == '__main__':
    warning_led_sim()

    rospy.spin()
