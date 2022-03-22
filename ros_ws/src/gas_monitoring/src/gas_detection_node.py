#!/usr/bin/env python3

# imports
import rospy
from std_msgs.msg import String, Bool, UInt16


class GasDetectionNode:
    # A Global Boolean that keeps track if Gas (either CO or Propane) is detected
    gas_flag = False

    # Stores current levels of Gases
    co_level = 0
    propane_level = 0

    # Stores Thresholds for the gases
    co_theshold = 1100
    propane_threshold = 4500

    # Set Emotions
    emots = None

    # Constructor for the class GasDetectionNode
    def __init__(self):
        # Setting up the ROS Node to be able to communicate with Arduino
        rospy.init_node('Gas_Detection_Node', anonymous=True)

        # Subscribe to the Gas Sensors
        rospy.Subscriber('gas_simulation', String, self.check_gas_data)

        rospy.spin()


    # Relays Gas Levels forward to toggle LED, start buzzer or send notification to GasMonitoringNode (if required)
    def relay_gas_levels(self):

        # Toggle buzzer for gas
        run_buzzer = rospy.Publisher("Gas_Buzzer", UInt16, queue_size=10)
        
        # Toggle LED Blinks
        blink_led = rospy.Publisher('Gas_Warning_LEDs', Bool, queue_size=10)
        
        # Notifing Monitoring station
        monitor_station = rospy.Publisher('Detection_Notification', String, queue_size=10)
        
        # Emotion Manager
        update_emotion = rospy.Publisher('Gas_Mon_Emotion', UInt16, queue_size=10)
        
        blink_led.publish(self.gas_flag)

        if self.gas_flag == False:
            run_buzzer.publish(0)
            update_emotion.publish(0)

        if self.gas_flag == True:
            
            monitor_station.publish("Gas Detected! - ")

            if self.co_level >= self.co_theshold:
                if self.propane_level >= self.propane_threshold:
                    run_buzzer.publish(3)
                    monitor_station.publish("Both\n")
                    update_emotion.publish(2)
                else:
                    run_buzzer.publish(1)
                    monitor_station.publish("CO\n")
                    update_emotion.publish(1)
                
            if self.propane_level >= self.propane_threshold:
                run_buzzer.publish(2)
                monitor_station.publish("Propane\n")
                update_emotion.publish(1)

            self.gas_flag = False
        
        rate_publishing = rospy.Rate(1) 
        rate_publishing.sleep()


    # Checks and Compares the thresholds of the Gases
    def check_threshold(self):

        # simulation of Gas Present Condition for CO and Propane
        # Needs to be updated for the correct values 
        # of concentration during testing of sensors
        if self.co_level >= self.co_theshold:
            rospy.loginfo("CO PRESENT!!!")
            self.gas_flag = True
            print('\a')

        if self.propane_level >= self.propane_threshold:
            rospy.loginfo("Propane DETECTED!!!")
            self.gas_flag = True
            print('\a')
        
        self.relay_gas_levels()


    # Receives the Data from the sensors and compares it with respective thresholds
    def check_gas_data(self, data):
        # obtained data from the sensor
        concs = [x for x in data.data.split(" ")]

        self.co_level = int(concs[0])
        self.propane_level = int(concs[1])

        self.check_threshold()


if __name__ == "__main__":
    gdn = GasDetectionNode()
