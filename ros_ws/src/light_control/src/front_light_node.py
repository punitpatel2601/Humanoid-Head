#!/usr/bin/env python3

#imports
import rospy
from std_msgs.msg import UInt16, Bool

# Class to monitor the light based on the inputs
class FrontLightNode:

    # Stores the values of two sensors
    sensor_f = 0
    sensor_r = 0

    # Light threshold at which we want the light to operate
    light_thres = 750

    # Stores different levels of light required
    new_lvl = 0
    last_lvl = new_lvl
    curr_lvl = 0
    change = 0

    def __init__(self):
        rospy.init_node('Light_Controller', anonymous=True)

        # Listen to the data from light sensor channels
        rospy.Subscriber('Front_Light_Sensor', UInt16, self.front_data)
        rospy.Subscriber('Back_Light_Sensor', UInt16, self.back_data)

        rospy.spin()

    # Sets the data from the front light sensor
    def front_data(self, received):
        self.sensor_f = received.data
        print("Front detection is ", self.sensor_f)

    # Sets the data from the rear light sensor
    def back_data(self, received):
        self.sensor_r = received.data
        print("Back Detection is ", self.sensor_r)

        self.sensor_data()
        

    # Turns on or off of output light on Robot
    def sensor_data(self):
        # Create the channels to publish the data
        ull = rospy.Publisher("Update_Light_Lumens", UInt16, queue_size=10)
        light_emo = rospy.Publisher("Light_Emotion", UInt16, queue_size=10)
        rate = rospy.Rate(1)

        # Calculations of the new light level required to be set
        self.curr_lvl = self.sensor_f+ self.sensor_r
        self.new_lvl = (self.light_thres - (self.curr_lvl/2)) * 0.95
        if self.last_lvl < self.new_lvl:
            light_emo.publish(1)
        else:
            light_emo.publish(0)
        if self.new_lvl < 0:
            self.new_lvl = 0

        # Set this level as last level for new calculations
        self.last_lvl = self.new_lvl
        
        # Send the data to robot
        ull.publish(int(self.new_lvl))

        rate.sleep()
        


if __name__ == '__main__':
    fln = FrontLightNode()