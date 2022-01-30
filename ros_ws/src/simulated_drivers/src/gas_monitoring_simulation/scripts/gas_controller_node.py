#!/usr/bin/env python3
# license removed for brevity
import rospy
from std_msgs.msg import String

def gas_controller_node():
    pub = rospy.Publisher('gas_monitor', String, queue_size=10)
    rospy.init_node('gas_controller_node', anonymous=True)
    rate = rospy.Rate(1)
    
    ppm = -500

    while not rospy.is_shutdown():
        gas_concentration = "Gas Concentration (ppm) = {}".format(ppm)
        rospy.loginfo(gas_concentration)
        pub.publish(str(ppm))
        ppm += 100

        if(ppm == 10000):
            ppm = 0

        rate.sleep()

if __name__ == '__main__':
    try:
        gas_controller_node()
    except rospy.ROSInterruptException:
        pass