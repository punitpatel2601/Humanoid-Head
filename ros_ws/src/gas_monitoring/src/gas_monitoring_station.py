#!/usr/bin/env python3

# imports
import rospy
from std_msgs.msg import String, Bool


# A Global Boolean that keeps track if Gas (either CO or Propane) is detected
gas_flag = False


# Turns on the warning lights on robot for gas detection
def toggle_warning_lights():
    led_blink = rospy.Publisher('gas_detected_led_warning_sim', Bool, queue_size=10)
    rate_led = rospy.Rate(1)

    global gas_flag
    led_blink.publish(gas_flag)
    gas_flag = False

    rate_led.sleep()


# Checks and Compares the thresholds of the Gases
def check_threshold(co, propane):
    global gas_flag
    
    # simulation of Gas Present Condition for CO and Propane
    # Needs to be updated for the correct values 
    # of concentration during testing of sensors
    if int(co) >= 1100:
        rospy.loginfo("CO PRESENT!!!")
        gas_flag = True
        print('\a')

    if int(propane) >= 4500:
        rospy.loginfo("Propane DETECTED!!!")
        gas_flag = True
        print('\a')
    
    toggle_warning_lights()


# Receives the Data from the sensors and compares it with respective thresholds
def check_gas_data(data):
    # obtained data from the sensor
    concs = [x for x in data.data.split(" ")]

    check_threshold(concs[0], concs[1])


# simulates the monitoring station for the robot       
def gas_monitoring_station():
    # Setting up the ROS Node to be able to communicate with Arduino
    rospy.init_node('gas_monitor_sim', anonymous=True)

    # Subscribe to the Gas Sensors
    rospy.Subscriber('gas_simulation', String, check_gas_data)


    
if __name__ == '__main__':
    gas_monitoring_station()

    rospy.spin()
