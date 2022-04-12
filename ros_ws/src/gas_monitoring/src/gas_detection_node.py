#!/usr/bin/env python3

# imports
import rospy
from std_msgs.msg import String, Bool, UInt16


class GasDetectionNode:
    # A Global Boolean that keeps track if Gas (either CO or Propane) is detected
    co_flag = False
    pro_flag = False

    # Stores current levels of Gases
    co_level = 0
    propane_level = 0

    # Last levels of Gases
    co_last = 0
    prop_last = 0

    # Stores Thresholds for the gases
    # These can be changed to trigger alarm sooner or later
    co_theshold = 400
    propane_threshold = 700


    # Constructor for the class GasDetectionNode
    def __init__(self):
        # Setting up the ROS Node to be able to communicate with Arduino
        rospy.init_node('Gas_Detection_Node', anonymous=True)

        rospy.Subscriber('MQ6_Sensor', UInt16, self.prop_gas_data)
        rospy.Subscriber('MQ7_Sensor', UInt16, self.co_gas_data)

        rospy.spin()


    # Relays Gas Levels forward to toggle LED, start buzzer or send notification to GasMonitoringNode (if required)
    def relay_gas_levels(self):

        # Toggle buzzer for gas
        run_buzzer = rospy.Publisher("Gas_Buzzer", UInt16, queue_size=10)
        
        # Toggle LED Blinks
        blink_co_led = rospy.Publisher('CO_Warning_LED', UInt16, queue_size=10)
        blink_prop_led = rospy.Publisher('Prop_Warning_LED', UInt16, queue_size=10)
        
        # Notifing Monitoring station
        monitor_station = rospy.Publisher('Detection_Notification', String, queue_size=10)
        
        # Emotion Manager
        update_emotion = rospy.Publisher('Gas_Emotion', UInt16, queue_size=10)
      
        # Turn off the buzzer if no gas is detected
        if self.co_flag == False and self.pro_flag == False:
            run_buzzer.publish(0)
            monitor_station.publish("\nNo Gas Detected...")
            # No gas above threshold but increasing alarmingly
            if (self.propane_level >= self.propane_threshold / 2) or (self.co_level >= self.co_theshold / 2):
                if self.co_level > self.co_last or self.propane_level > self.prop_last:
                    update_emotion.publish(2)
                else:
                    update_emotion.publish(0)
            else:
                update_emotion.publish(0)

        # Turn on/off respective things for gas detection
        if self.co_flag == True:
            update_emotion.publish(1)
            monitor_station.publish("\nDetected Gas - ")
            run_buzzer.publish(100)
            blink_co_led.publish(1024 - self.co_level)
            monitor_station.publish("CO\t")

            self.co_flag = False

        if self.pro_flag == True:
            update_emotion.publish(1)
            monitor_station.publish("\nDetected Gas - ")
            run_buzzer.publish(200)
            blink_prop_led.publish(1024 - self.propane_level)
            monitor_station.publish("Propane\t")

            self.pro_flag = False

        # If both gases detected, change buzzer tone
        if self.pro_flag == True and self.co_flag == True:
            run_buzzer.publish(50)
        
        self.co_last = self.co_level
        self.prop_last = self.propane_level

        rate_publishing = rospy.Rate(1) 
        rate_publishing.sleep()


    # Checks and Compares the thresholds of the Gases
    def check_co_threshold(self):
        # simulation of Gas Present Condition for CO and Propane
        if self.co_level >= self.co_theshold:
            rospy.loginfo("CO PRESENT!!!")
            self.co_flag = True
        
        self.relay_gas_levels()

    # Checks and Compares the thresholds of the Gases
    def check_prop_threshold(self):
        # simulation of Gas Present Condition for CO and Propane
        if self.propane_level >= self.propane_threshold:
            rospy.loginfo("Propane PRESENT!!!")
            self.pro_flag = True
        


    # Receives the Data from the sensors and compares it with respective thresholds
    def co_gas_data(self, data):
        # obtained data from the sensor
        self.co_level = data.data
        print(self.co_level)
        self.check_co_threshold()

    # Receives the Data from the sensors and compares it with respective thresholds
    def prop_gas_data(self, data):
        # obtained data from the sensor
        self.propane_level = data.data
        print(self.propane_level)
        self.check_prop_threshold()


if __name__ == "__main__":
    gdn = GasDetectionNode()
