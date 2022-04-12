#!/usr/bin/env python3 

import rospy
from std_msgs.msg import String

# Class that recieves information of the Gas detected from the detection node
class GasMonitoringNode:

    def __init__(self):
        rospy.init_node('Gas_Monitoring_Node', anonymous=True)

        # Listen to the data sent from Detection Node
        rospy.Subscriber('Detection_Notification', String, self.notification)

        rospy.spin()

    # Read and Display the detected Gas
    def notification(self, detection_msg):
        rospy.loginfo(detection_msg.data)


if __name__ == "__main__":
    gmn = GasMonitoringNode()
