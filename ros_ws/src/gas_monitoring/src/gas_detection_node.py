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

    # Last levels of Gases
    co_last = 0
    prop_last = 0

    # Stores Thresholds for the gases
    co_theshold = 1100
    propane_threshold = 4500


    # Constructor for the class GasDetectionNode
    def __init__(self):
        # Setting up the ROS Node to be able to communicate with Arduino
        rospy.init_node('Gas_Detection_Node', anonymous=True)

        rospy.Subscriber('MQ7', UInt16, self.co_gas_data)
        rospy.Subscriber('MQ6', UInt16, self.prop_gas_data)

        rospy.spin()


    # Relays Gas Levels forward to toggle LED, start buzzer or send notification to GasMonitoringNode (if required)
    def relay_gas_levels(self, gas_id):

        # Toggle buzzer for gas
        run_buzzer = rospy.Publisher("Gas_Buzzer", UInt16, queue_size=10)
        
        # Toggle LED Blinks
        blink_co_led = rospy.Publisher('CO_Warning_LED', Bool, queue_size=10)
        blink_prop_led = rospy.Publisher('Prop_Warning_LED', Bool, queue_size=10)
        
        # Notifing Monitoring station
        monitor_station = rospy.Publisher('Detection_Notification', String, queue_size=10)
        
        # Emotion Manager
        update_emotion = rospy.Publisher('Gas_Emotion', UInt16, queue_size=10)
        
        
        # Blink the lights based on the gas flag - true is detected, false if not detected
        if gas_id == 1:
            blink_co_led.publish(self.gas_flag)
        elif gas_id == 2:
            blink_prop_led.publish(self.gas_flag)

        # Turn off the buzzer if no gas is detected
        if self.gas_flag == False:
            run_buzzer.publish(0)
            monitor_station.publish("\nNo Gas Detected...")
            # No gas above threshold but increasing alarmingly
            if self.propane_level >= self.propane_threshold / 2 or self.co_level >= self.co_theshold / 2:
                if self.co_level > self.co_last or self.propane_level > self.prop_last:
                    update_emotion.publish(2)
                else:
                    update_emotion.publish(0)
            else:
                update_emotion.publish(0)

        # Turn of respective things for gas detection
        if self.gas_flag == True:
            
            update_emotion.publish(1)
            monitor_station.publish("\nDetected Gas - ")
            
            if self.co_level >= self.co_theshold and self.propane_level >= self.propane_threshold:
                run_buzzer.publish(7)
                monitor_station.publish("Both\t")
            elif self.co_level >= self.co_theshold:
                run_buzzer.publish(1)
                monitor_station.publish("CO\t")
            elif self.propane_level >= self.propane_threshold:
                run_buzzer.publish(2)
                monitor_station.publish("Propane\t")

            self.gas_flag = False
        
        self.co_last = self.co_level
        self.prop_last = self.propane_level

        rate_publishing = rospy.Rate(1) 
        rate_publishing.sleep()


    # Checks and Compares the thresholds of the Gases
    def check_co_threshold(self):
        # simulation of Gas Present Condition for CO and Propane
        # Needs to be updated for the correct values 
        # of concentration during testing of sensors
        if self.co_level >= self.co_theshold:
            rospy.loginfo("CO PRESENT!!!")
            self.gas_flag = True
        
        self.relay_gas_levels(1)

    # Checks and Compares the thresholds of the Gases
    def check_prop_threshold(self):
        # simulation of Gas Present Condition for CO and Propane
        # Needs to be updated for the correct values 
        # of concentration during testing of sensors
        if self.propane_level >= self.propane_threshold:
            rospy.loginfo("Propane PRESENT!!!")
            self.gas_flag = True
        
        self.relay_gas_levels(2)


    # Receives the Data from the sensors and compares it with respective thresholds
    def co_gas_data(self, data):
        # obtained data from the sensor
        self.co_level = data.data
        self.check_co_threshold()

    # Receives the Data from the sensors and compares it with respective thresholds
    def prop_gas_data(self, data):
        # obtained data from the sensor
        self.propane_level = data.data
        self.check_prop_threshold()


if __name__ == "__main__":
    gdn = GasDetectionNode()
