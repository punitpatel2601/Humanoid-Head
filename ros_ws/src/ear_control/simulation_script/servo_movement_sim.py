#!/usr/bin/env python3

import rospy
from std_msgs.msg import UInt16

def right_ear(data):

    print("\nRight Ear at: " + str(data.data))



def left_ear(data):

    print("Left Ear at: " + str(data.data))


def move_servos():
    rospy.init_node("servos_simulation", anonymous=True)

    rospy.Subscriber('Right_Ear_Controller', UInt16, right_ear)
    rospy.Subscriber('Left_Ear_Controller', UInt16, left_ear)


if __name__ == '__main__':
    move_servos()

    rospy.spin()
