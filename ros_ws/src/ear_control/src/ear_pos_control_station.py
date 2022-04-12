#!/usr/bin/env python3 

import rospy
from std_msgs.msg import UInt16


def manual_ear_positioning():
    # Set up channel
    manu_pub = rospy.Publisher('Manual_Ear_Controller', UInt16, queue_size=10)

    rospy.init_node('Ear_Positioning_Station', anonymous=True)
    rate = rospy.Rate(1)

    while not rospy.is_shutdown():
        # Get the emotion ID
        emo_id = input("Enter ID (0 Idle, 1 Danger, 2 Caution):")

        # Set the emotion
        manu_pub.publish(int(emo_id))

        rate.sleep()


if __name__ == '__main__':
    try:
        manual_ear_positioning()
    except rospy.ROSInterruptException:
        pass

