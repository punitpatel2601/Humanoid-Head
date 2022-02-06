#!/usr/bin/env python3

import rospy
import emotions
from std_msgs.msg import UInt16


def select_emotion(id):
    if int(id%3) == 0:
        print("Danger\n")
        return emotions.Danger
    elif int(id/2) == 0:
        print("Sad\n")
        return emotions.Sad
    else:
        print("Happy\n")
        return emotions.Happy



def ear_controller():
    right_angle_publisher = rospy.Publisher('Right_Ear_Controller', UInt16, queue_size=10)
    left_angle_publisher = rospy.Publisher('Left_Ear_Controller', UInt16, queue_size=10)

    rospy.init_node('Ear_Controller', anonymous=True)
    rate = rospy.Rate(1)

    # following snippet simulates different emotions (hard coded)
    # would be updated so that it is automatic later on
    # and try to make it relevant to what robot is experiencing

    i = 0

    while not rospy.is_shutdown():
        
        i += 1
        emotion_selected = select_emotion(i)
    
        # send the ear angles to the robot
        right_angle_publisher.publish(emotion_selected[0])
        left_angle_publisher.publish(emotion_selected[1])

        rate.sleep()


if __name__ == '__main__':
    try:
        ear_controller()
    except rospy.ROSInterruptException:
        pass
