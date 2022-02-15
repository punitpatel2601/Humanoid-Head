#!/usr/bin/env python3

# imports
from numpy import rate
import rospy
from std_msgs.msg import UInt16, Bool


# simulates the turning on and off of led on Robot
def update_light(recieved):
    rospy.loginfo("Light lumens is: ")
    rospy.loginfo(recieved.data)

    ull = rospy.Publisher("Update_Light_Lumens", Bool, queue_size=10)
    rate = rospy.Rate(1)
    ull.publish(True)
    rate.sleep()

def warning_led_sim():
    # subscribe and listen the data from gas monitoring service
    rospy.init_node('Light_Controller', anonymous=True)

    rospy.Subscriber('light_simulation', UInt16, update_light)



if __name__ == '__main__':
    warning_led_sim()

    rospy.spin()
