#!/usr/bin/env python3
import rospy
from std_msgs.msg import String

def callback(data):
    ppm = int(data.data)

    if(ppm >= 4500):
        rospy.loginfo("Propane Detected with concentration - " + str(ppm))
    elif(ppm >= 1400):
        rospy.loginfo("CO Detected with concentration - " + str(ppm))
    
    
def listener():
    rospy.init_node('gas_sensor_node', anonymous=True)

    rospy.Subscriber('gas_monitor', String, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()