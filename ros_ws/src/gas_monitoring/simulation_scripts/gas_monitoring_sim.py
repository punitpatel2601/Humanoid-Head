#!/usr/bin/env python3

# imports
import rospy
from std_msgs.msg import String, Bool


# boolean to determine if any gas detected
flag = False


# turn on the led on robot if gas detected
def send_led_status():
    led_blink = rospy.Publisher('gas_detected_led_warning_sim', Bool, queue_size=10)
    rate_led = rospy.Rate(1)

    global flag
    led_blink.publish(flag)
    flag = False

    rate_led.sleep()


# check the threshold for the gases (CO and Propane)
def check_threshold(co, propane):

    # changes the flag outside the function
    global flag

    # simulation of Gas Present Condition for CO and Propane
    if int(co) >= 1100:
        rospy.loginfo("CO PRESENT!!!")
        flag = True
        print('\a')

    if int(propane) >= 4500:
        rospy.loginfo("Propane DETECTED!!!")
        flag = True
        print('\a')
    
    send_led_status()


def callback(data):

    # obtained data from the (simulated) sensor
    concs = [x for x in data.data.split(" ")]

    check_threshold(concs[0], concs[1])


# simulates the monitoring station for the robot       
def gas_monitoring_sim():
    rospy.init_node('gas_monitor_sim', anonymous=True)

    rospy.Subscriber('gas_simulation', String, callback)


    
if __name__ == '__main__':
    gas_monitoring_sim()

    rospy.spin()
    