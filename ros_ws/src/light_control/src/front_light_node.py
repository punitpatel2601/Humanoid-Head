#!/usr/bin/env python3

#imports
import rospy
from std_msgs.msg import UInt16, Bool


class FrontLightNode:

    sensor_f = 0
    sensor_r = 0

    light_thres = 750

    new_lvl = 0
    last_lvl = new_lvl
    curr_lvl = 0
    change = 0

    def __init__(self):
        rospy.init_node('Light_Controller', anonymous=True)

        rospy.Subscriber('Front_Light_Sensor', UInt16, self.front_data)
        rospy.Subscriber('Back_Light_Sensor', UInt16, self.back_data)

        rospy.spin()

    def front_data(self, received):
        self.sensor_f = received.data
        print("Front detection is ", self.sensor_f)

    def back_data(self, received):
        self.sensor_r = received.data
        print("Back Detection is ", self.sensor_r)

        self.sensor_data()
        

    # simulates the turning on and off of led on Robot
    def sensor_data(self):
        ull = rospy.Publisher("Update_Light_Lumens", UInt16, queue_size=10)
        light_emo = rospy.Publisher("Light_Emotion", UInt16, queue_size=10)
        rate = rospy.Rate(1)

        self.curr_lvl = self.sensor_f+ self.sensor_r
        self.new_lvl = (self.light_thres - (self.curr_lvl/2)) * 0.95

        if self.last_lvl < self.new_lvl:
            light_emo.publish(1)
        else:
            light_emo.publish(0)

        if self.new_lvl < 0:
            self.new_lvl = 0

        self.last_lvl = self.new_lvl
        
        print(int(self.new_lvl))
        ull.publish(int(self.new_lvl))

        rate.sleep()
        


if __name__ == '__main__':
    fln = FrontLightNode()