#!/usr/bin/env python3

# imports
import rospy
from std_msgs.msg import UInt16

emo_id = 0

# EMOTION_NAME = [RIGHT EAR SERVO ANGLE, LEFT EAR SERVO ANGLE]
Idle = [90, 90]
Danger = [180, 180]
Caution = [0, 0]


# Flags to priortize emotions
gas_flag = False
manual_flag = False
light_flag = False

gas_emot = Idle
man_emot = Idle
light_flag = Idle
default_emot = Idle


# Sets overall emotion - prioritizing gas, followed by manual
def set_emotion():
    if gas_flag == True:
        return gas_emot
    elif manual_flag == True:
        return man_emot
    elif light_flag == True:
        return light_emot
    else:
        return default_emot


# Emotion set by operator
def man_set_emotion(id):
    global manual_flag, man_emot
    if id == 1:
        manual_flag = True
        print("Man - Danger\n")
        man_emot = Danger
    elif id == 2:
        manual_flag = True
        print("Man - Caution\n")
        man_emot = Caution
    else:
        manual_flag = False
        
# Emotions set by gas monitoring node
def gas_selected_emotion(id):  
    global gas_flag, gas_emot
    if id == 1:
        gas_flag = True
        print("Gas - Danger\n")
        gas_emot = Danger
    elif id == 2:
        gas_flag = True
        print("Gas - Caution\n")
        gas_emot = Caution
    else:
        gas_flag = False
        print("Idle\n")

# Emotions set by gas monitoring node
def light_selected_emotion(id):  
    global light_flag, light_emot
    if id == 1:
        light_flag = True
        print("Light - Caution\n")
        light_emot = Caution
    else:
        light_flag = False
        print("Idle\n")


def change_emotion(message):
    gas_selected_emotion(message.data)

def manual_emotion(message):
    man_set_emotion(message.data)

def light_emotion(message):
    light_selected_emotion(message.data)


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
    rospy.Subscriber('Light_Emotion', UInt16, light_emotion)
    
    while not rospy.is_shutdown():
        emotion_selected = set_emotion()
        
        # send the ear angles to the robot
        right_angle_publisher.publish(emotion_selected[0])
        left_angle_publisher.publish(emotion_selected[1])

        rate.sleep()


if __name__ == '__main__':
    try:
        ear_controller()
    except rospy.ROSInterruptException:
        pass
