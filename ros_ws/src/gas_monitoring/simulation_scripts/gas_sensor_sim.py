#!/usr/bin/env python3

# imports
import rospy
from std_msgs.msg import String


# simulates the sensor
def gas_sensor_sim():
    # publish the sensor data
    pub = rospy.Publisher('gas_simulation', String, queue_size=10)
    rospy.init_node('gas_sensor_sim', anonymous=True)
    rate = rospy.Rate(1)
    
    # variables to store the concentrations
    co_ppm = 0
    pro_ppm = 0

    while not rospy.is_shutdown():
        
        # simulates the data obtained by the sensor
        co_ppm = input("Enter CO Concentration: ")
        pro_ppm = input("Enter Propane Concentration: ")
        
        '''
        co_conc = "CO Concentration (ppm) = {}".format(co_ppm)
        pro_conc = "Propane Concentration (ppm) = {}".format(pro_ppm)
        '''

        # send gas concentration to monitoring station
        data_obtained = str(co_ppm) + " " + str(pro_ppm)

        # rospy.loginfo(co_conc + "\n" + pro_conc + "\n")
        pub.publish(data_obtained)

        rate.sleep()



if __name__ == '__main__':
    try:
        gas_sensor_sim()
    except rospy.ROSInterruptException:
        pass