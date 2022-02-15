#!/usr/bin/env python3

# imports
import rospy
from std_msgs.msg import UInt16


# simulates the turning on and off of led on Robot
def turn_buzzer(recieved):
    if recieved.data is 0:
        rospy.loginfo("Buzzer (on Robot) is turned OFF")
    else:
        rospy.loginfo("Buzzer (on Robot) is turned ON")


def warning_led_sim():
    # subscribe and listen the data from gas monitoring service
    rospy.init_node('Buzzer', anonymous=True)

    rospy.Subscriber('Gas_Buzzer', UInt16, turn_buzzer)



if __name__ == '__main__':
    warning_led_sim()

    rospy.spin()
