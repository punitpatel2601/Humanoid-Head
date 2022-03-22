#!/usr/bin/env python3

# imports
import rospy
from std_msgs.msg import Bool


# simulates the turning on and off of led on Robot
def turn_led(data):
    if data.data is True:
        rospy.loginfo("Warning LED (on Robot) is turned ON")
    else:
        rospy.loginfo("Warning LED (on Robot) is turned OFF")


def warning_led_sim():
    # subscribe and listen the data from gas monitoring service
    rospy.init_node('LED', anonymous=True)

    rospy.Subscriber('Gas_Warning_LEDs', Bool, turn_led)



if __name__ == '__main__':
    warning_led_sim()

    rospy.spin()
