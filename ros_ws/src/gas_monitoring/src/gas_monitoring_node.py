#!/usr/bin/env python3 

import rospy
from std_msgs.msg import String


class GasMonitoringNode:

    def __init__(self):
        rospy.init_node('Monitoring_Station', anonymous=True)

        rospy.Subscriber('detection_notification', String, self.notification)

        rospy.spin()

    def notification(self, detection_msg):
        print(detection_msg.data)


if __name__ == "__main__":
    gmn = GasMonitoringNode()
