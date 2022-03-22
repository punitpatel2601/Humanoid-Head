#!/usr/bin/env python3

#imports
from numpy import rate
import rospy
from std_msgs.msg import UInt16, Bool


class FrontLightNode:

    sensor_max = 1023
    sensor_mix = 0

    light_thres = 750

    new_lvl = 0
    curr_lvl = 0
    change = 0

    def __init__(self):

        rospy.init_node('Light_Controller', anonymous=True)

        rospy.Subscriber('light_sensor', UInt16, self.sensor_data)

    # simulates the turning on and off of led on Robot
    def sensor_data(self, received):
        rospy.loginfo("Light lumens is: ")
        rospy.loginfo(received.data)

        self.req_updates(received.data)


    def req_updates(self, data):
        ull = rospy.Publisher("Update_Light_Lumens", UInt16, queue_size=10)
        rate = rospy.Rate(1)

        self.curr_lvl = data
        self.change = self.light_thres - self.curr_lvl

        if self.curr_lvl <= self.light_thres:
            self.new_lvl += (self.change / 0.9)
        else:
            self.new_lvl -= (self.change / 0.9)

        ull.publish(self.new_lvl)


if __name__ == '__main__':
    fln = FrontLightNode()