#!/usr/bin/env python3
import rospy
from std_msgs.msg import String


def check_threshold(co, propane):
    if int(co) >= 1100:
        rospy.loginfo("CO PRESENT!!!")
        print('\a')

    if int(propane) >= 4500:
        rospy.loginfo("Propane DETECTED!!!")
        print('\a')
        print('\a')


def callback(data):
    concs = [x for x in data.data.split(" ")]

    check_threshold(concs[0], concs[1])
    
    
def gas_monitoring_sim():
    rospy.init_node('gas_monitor_sim', anonymous=True)

    rospy.Subscriber('gas_simulation', String, callback)
    rospy.spin()

if __name__ == '__main__':
    gas_monitoring_sim()