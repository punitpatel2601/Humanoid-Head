#!/usr/bin/env python3

# imports
import rospy
from std_msgs.msg import String, UInt16


# simulates the sensor
def gas_sensor_sim():
    # publish the sensor data
    mq6 = rospy.Publisher('MQ6', UInt16, queue_size=10)
    mq7 = rospy.Publisher('MQ7', UInt16, queue_size=10)

    rospy.init_node('gas_sensor_sim', anonymous=True)
    
    rate = rospy.Rate(1)
    
    # variables to store the concentrations
    co_ppm = 0
    pro_ppm = 0

    while not rospy.is_shutdown():
        
        # simulates the data obtained by the sensor
        co_ppm = input("Enter CO Concentration: ")
        pro_ppm = input("Enter Propane Concentration: ")
        
        mq7.publish(int(co_ppm))
        mq6.publish(int(pro_ppm))

        rate.sleep()



if __name__ == '__main__':
    try:
        gas_sensor_sim()
    except rospy.ROSInterruptException:
        pass
