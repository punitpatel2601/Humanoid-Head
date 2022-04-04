#!/usr/bin/env python3

# imports
import rospy
import emotions
from std_msgs.msg import UInt16

emo_id = 0

def change_emotion(message):
    emotions.gas_selected_emotion(message.data)

def manual_emotion(message):
    emotions.man_set_emotion(message.data)

# Controls the ears by sending the angle data to Arduino Board
def ear_controller():
    # Channels for sending angles for each ears
    right_angle_publisher = rospy.Publisher('Right_Ear_Controller', UInt16, queue_size=10)
    left_angle_publisher = rospy.Publisher('Left_Ear_Controller', UInt16, queue_size=10)

    # Setting up the ROS Node to be able to communicate with Arduino
    rospy.init_node('Ear_Controller', anonymous=True)
    rate = rospy.Rate(1)

    rospy.Subscriber('Manual_Ear_Controller', UInt16, manual_emotion)
    rospy.Subscriber('Gas_Emotion', UInt16, change_emotion)
    
    while not rospy.is_shutdown():
        emotion_selected = emotions.set_emotion()
        
        print(emotion_selected)
        # send the ear angles to the robot
        right_angle_publisher.publish(emotion_selected[0])
        left_angle_publisher.publish(emotion_selected[1])

        rate.sleep()


if __name__ == '__main__':
    try:
        ear_controller()
    except rospy.ROSInterruptException:
        pass
