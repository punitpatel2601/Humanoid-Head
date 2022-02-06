#include <ros.h>
#include <ArduinoHardware.h>
#include <std_msgs/String.h>
#include <std_msgs/Bool.h>
#include <std_msgs/UInt16.h>
#include <Servo.h>


//********************** TESTING IN PROGRESS



// Setting the pins on board for

// Inputs (Sensors, Switches, etc.)
// #define GAS_SENSOR <PIN>NUMBER>
// #define LIGHT_SENSOR <PIN_NUMBER>

// Outputs (LEDs, Motors, Sounds, etc.)
#define GAS_WARN_LED 13
#define SERVO_MOTOR 9


// global variables
ros::NodeHandle nh;
std_msgs::String gas_reading;

Servo servo;


// Toggle LED light when the gas is detected
void toggle_warning_led(const std_msgs::Bool led_toggle)
{
  if (led_toggle.data == true)
    digitalWrite(GAS_WARN_LED, HIGH);
  else
    digitalWrite(GAS_WARN_LED, LOW);
}

// Updates the servo angle
void change_ear_angle(const std_msgs::UInt16 &servo_command){
  servo.write(servo_command.data); //set the servo angle between 0 to 180
}


// List of publishers and Subscribers to ROS
ros::Publisher gas_Sensor_Reading("Gas_Sensor", &gas_reading);
ros::Subscriber<std_msgs::Bool> warning_Led("Toggle_Warning_LED", toggle_warning_led);

/*
ros::Publisher light_Sensor_Reading("Light_Sensor", &light_reading);
ros::Subscriber<std_msgs::Int64t> change_Light("Update_Light:, &update_light_intensity);
*/

ros::Subscriber<std_msgs::UInt16> servo_Updates("Ear_Controller", change_ear_angle);



void setup()
{
  pinMode(GAS_WARN_LED, OUTPUT);
  // pinMode(GAS_SENSOR, INPUT);

  nh.initNode();

  // Gas Monitoring
  nh.advertise(gas_Sensor_Reading);
  nh.subscribe(warning_Led);

  // Ear Positioning
  nh.subscribe(servo_Updates);
  servo.attach(SERVO_MOTOR);
}


void loop()
{
  std_msgs::String gas_reads;
  // gas_reads = <data from sensor at whatever pin it is>
  
  gas_reads.data = "1500 3500";
  gas_Sensor_Reading.publish(&gas_reads);

  nh.spinOnce();

  delay(1000);
}
