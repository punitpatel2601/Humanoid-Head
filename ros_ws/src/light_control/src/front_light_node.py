#!/usr/bin/env python3

#imports
from hashlib import new
import rospy
from std_msgs.msg import UInt16, Bool


class FrontLightNode:

    sensor_max = 1023
    sensor_mix = 0

    light_thres = 750

    new_lvl = 0
    last_lvl = new_lvl
    curr_lvl = 0
    change = 0

    def __init__(self):
        rospy.init_node('Light_Controller', anonymous=True)

        rospy.Subscriber('light_sensor', UInt16, self.sensor_data)

        rospy.spin()

        

    # simulates the turning on and off of led on Robot
    def sensor_data(self, received):
        rospy.loginfo("Light lumens is: ")
        rospy.loginfo(received.data)

        ull = rospy.Publisher("Update_Light_Lumens", UInt16, queue_size=10)
        light_emo = rospy.Publisher("Light_Emotion", UInt16, queue_size=10)
        rate = rospy.Rate(1)

        self.curr_lvl = received.data
        self.change = self.light_thres - self.curr_lvl

        self.new_lvl = (self.change * 0.95)

        if self.last_lvl > self.new_lvl:
            light_emo.publish(1)
        else:
            light_emo.publish(0)

        if self.new_lvl < 0:
            self.new_lvl = 0
        
        print(int(self.new_lvl))

        ull.publish(int(self.new_lvl))

        rate.sleep()
        


if __name__ == '__main__':
    fln = FrontLightNode()