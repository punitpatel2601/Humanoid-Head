#!/usr/bin/env python3

# imports
import rospy
from std_msgs.msg import String, Bool


class GasDetectionNode:
    # A Global Boolean that keeps track if Gas (either CO or Propane) is detected
    gas_flag = False


    def __init__(self):
        # Setting up the ROS Node to be able to communicate with Arduino
        rospy.init_node('gas_monitor_sim', anonymous=True)

        # Subscribe to the Gas Sensors
        rospy.Subscriber('gas_simulation', String, self.check_gas_data)

        rospy.spin()


    # Turns on the warning lights on robot for gas detection
    def toggle_warning_lights(self):
        # Toggle LED Blinks
        led_blink = rospy.Publisher('gas_detected_led_warning_sim', Bool, queue_size=10)
        led_blink.publish(self.gas_flag)

        # buzzer in this line publishing
        # update buzzer code here

        # Notifing Monitoring station
        monitor_station = rospy.Publisher('detection_notification', String, queue_size=10)
        if self.gas_flag == True:
            monitor_station.publish("Gas Detected!")
            self.gas_flag = False
        
        rate_publishing = rospy.Rate(1) 
        rate_publishing.sleep()


    # Checks and Compares the thresholds of the Gases
    def check_threshold(self, co, propane):

        # simulation of Gas Present Condition for CO and Propane
        # Needs to be updated for the correct values 
        # of concentration during testing of sensors
        if int(co) >= 1100:
            rospy.loginfo("CO PRESENT!!!")
            self.gas_flag = True
            print('\a')

        if int(propane) >= 4500:
            rospy.loginfo("Propane DETECTED!!!")
            self.gas_flag = True
            print('\a')
        
        self.toggle_warning_lights()


    # Receives the Data from the sensors and compares it with respective thresholds
    def check_gas_data(self, data):
        # obtained data from the sensor
        concs = [x for x in data.data.split(" ")]

        # check thresholds
        self.check_threshold(concs[0], concs[1])

if __name__ == "__main__":
    gdn = GasDetectionNode()
