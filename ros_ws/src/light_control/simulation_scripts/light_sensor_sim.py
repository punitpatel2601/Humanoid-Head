#!/usr/bin/env python3

# imports
import rospy
from std_msgs.msg import UInt16


# simulates the sensor
def light_sen_sim():
    # publish the sensor data
    pub = rospy.Publisher('light_simulation', UInt16, queue_size=10)
    rospy.init_node('light_sensor_sim', anonymous=True)
    rate = rospy.Rate(1)
    
    # variables to store the concentrations
    light_on = 0
    i = 0

    while not rospy.is_shutdown():
        
        if i <= 20:
            light_on += 10
            i+=1
        elif i > 0:
            light_on -= 10
            i-=15

        # send gas concentration to monitoring station
        data_obtained = light_on

        # rospy.loginfo(co_conc + "\n" + pro_conc + "\n")
        pub.publish(light_on)

        rate.sleep()



if __name__ == '__main__':
    try:
        light_sen_sim()
    except rospy.ROSInterruptException:
        pass
