#include <ros.h>
#include <ArduinoHardware.h>
#include <std_msgs/String.h>
#include <std_msgs/Bool.h>
#include <std_msgs/UInt16.h>
#include <Servo.h>


// Inputs (Sensors, Switches, etc.)
#define LIGHT_SENSOR_F A4	// Attach light sensor on A4
#define LIGHT_SENSOR_R A5	// Attach light sensor on A5

#define MQ6_SENSOR A0
#define MQ7_SENSOR A1

// Outputs (LEDs, Motors, Sounds, etc.)
#define BUZZER 11    		//Attach the buzzer to pin number 11
#define PROP_WARN_LED 13 	//Attach the warning led to pin number 13
#define CO_WARN_LED 12  	//Attach the warning led to pin number 12

#define RIGHT_EAR 5 		//Attach Right ear Servo to pin 5
#define LEFT_EAR 6  		//Attach Left ear Servo to pin 6

#define BLUE_LIGHT 9 		//Attach blue output light to pin 8

// global variables
ros::NodeHandle nh;		// ROS Node Handle

Servo rServo;			// Right Servo
Servo lServo;			// Left Servo
	
	
// Sends the Light sensor DATA
std_msgs::UInt16 light_val;
ros::Publisher front_light_sensor("Front_Light_Sensor", &light_val);
ros::Publisher back_light_sensor("Back_Light_Sensor", &light_val);

// Sends the Gas Sensor DATA
std_msgs::UInt16 gas_val;
ros::Publisher mq6_sensor("MQ6_Sensor", &gas_val);
ros::Publisher mq7_sensor("MQ7_Sensor", &gas_val);

// Listens to warning LED lights toggling DATA
ros::Subscriber<std_msgs::UInt16> co_warning_Led("CO_Warning_LED", toggle_co_led);
ros::Subscriber<std_msgs::UInt16> prop_warning_Led("Prop_Warning_LED", toggle_prop_led);

// Controls Gas Buzzer
ros::Subscriber<std_msgs::UInt16> gas_buzzer("Gas_Buzzer", run_gas_buzzer);

// Controls EAR Servos
ros::Subscriber<std_msgs::UInt16> right_servo("Right_Ear_Controller", update_rServo);
ros::Subscriber<std_msgs::UInt16> left_servo("Left_Ear_Controller", update_lServo);

// Updates the Output Light
ros::Subscriber<std_msgs::UInt16> blue_light("Update_Light_Lumens", update_outLight);



// Toggle LED light when the gas is detected
void toggle_co_led(const std_msgs::UInt16 & led_toggle)
{
  if (led_toggle.data > 0)
  {
    digitalWrite(CO_WARN_LED, HIGH);
    delay(led_toggle.data);
    digitalWrite(CO_WARN_LED, LOW);
    delay(led_toggle.data);
  }
  else
    digitalWrite(CO_WARN_LED, LOW);
}

// Toggle LED light when the gas is detected
void toggle_prop_led(const std_msgs::UInt16 & led_toggle)
{
  if (led_toggle.data > 0)
  {
    digitalWrite(PROP_WARN_LED, HIGH);
    delay(led_toggle.data);
    digitalWrite(PROP_WARN_LED, LOW);
    delay(led_toggle.data);
  }
  else
    digitalWrite(PROP_WARN_LED, LOW);
}

// Toggle Buzzer when the gas is detected
void run_gas_buzzer(const std_msgs::UInt16 & toggle_buzzer) {
  if (toggle_buzzer.data != 0) {
    analogWrite(BUZZER, toggle_buzzer.data);
    delay(toggle_buzzer.data);
    analogWrite(BUZZER, 0);
    delay(toggle_buzzer.data);
  }
  else
    analogWrite(BUZZER, 0);
}

// Update Servo angle to respond to emotion
void update_rServo(const std_msgs::UInt16 & angle) {
  rServo.write(angle.data);
}

// Update Servo angle
void update_lServo(const std_msgs::UInt16 & angle) {
  lServo.write(angle.data);
}

// Changes the output light
void update_outLight(const std_msgs::UInt16 & lumens) {
  analogWrite(BLUE_LIGHT, lumens.data);
  delay(100);
}

void setup()
{
  Serial.begin(57600);

// Set up and initialize the connections

  pinMode(LIGHT_SENSOR_F, INPUT);
  pinMode(LIGHT_SENSOR_R, INPUT);

  pinMode(MQ6_SENSOR, INPUT);
  pinMode(MQ7_SENSOR, INPUT);

  pinMode(BUZZER, OUTPUT);

  pinMode(CO_WARN_LED, OUTPUT);
  pinMode(PROP_WARN_LED, OUTPUT);

  pinMode(BLUE_LIGHT, OUTPUT);

  rServo.attach(RIGHT_EAR);
  lServo.attach(LEFT_EAR);

// Initialize the node and connect to ROS
  nh.initNode();

// Create channels to send sensor data
  nh.advertise(front_light_sensor);
  nh.advertise(back_light_sensor);

  nh.advertise(mq6_sensor);
  nh.advertise(mq7_sensor);

// Listen to channels to check incoming update requests
  nh.subscribe(co_warning_Led);
  nh.subscribe(prop_warning_Led);

  nh.subscribe(gas_buzzer);

  nh.subscribe(right_servo);
  nh.subscribe(left_servo);

  nh.subscribe(blue_light);
}

int light_v;
int gas_reads;

void loop()
{
// Send front light sensor data
  light_v = analogRead(A4);
  light_val.data = light_v;
  front_light_sensor.publish(&light_val);

  delay(250);

// Send rear light sensor data
  light_v = analogRead(A5);
  light_val.data = light_v;
  back_light_sensor.publish(&light_val);

  delay(250);
  
// Send Propane data
  gas_reads = analogRead(A0);
  gas_val.data = gas_reads;
  mq6_sensor.publish(&gas_val);

  delay(250);

// Send CO data
  gas_reads = analogRead(A1);
  gas_val.data = gas_reads;
  mq7_sensor.publish(&gas_val);

  delay(200);

// Wait for incoming data
  nh.spinOnce();
  delay(50);
}
