#!/usr/bin/env python3 

import rospy
from std_msgs.msg import String


class GasMonitoringNode:

    def __init__(self):
        rospy.init_node('Gas_Monitoring_Node', anonymous=True)

        rospy.Subscriber('Detection_Notification', String, self.notification)

        rospy.spin()

    def notification(self, detection_msg):
        rospy.loginfo(detection_msg.data)


if __name__ == "__main__":
    gmn = GasMonitoringNode()
