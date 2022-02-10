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
#define BUZZER 9    //Attach the buzzer to pin number 9
#define GAS_WARN_LED 13 //Attach the warning led to pin number 13

#define RIGHT_EAR 5 //Attach Right ear Servo to pin 5
#define LEFT_EAR 6  //Attach Left ear Servo to pin 6


// global variables
ros::NodeHandle nh;
std_msgs::String gas_reading;

Servo rServo;
Servo lServo;


// Toggle LED light when the gas is detected
void toggle_warning_led(const std_msgs::Bool led_toggle)
{
  if (led_toggle.data == true)
    digitalWrite(GAS_WARN_LED, HIGH);
  else
    digitalWrite(GAS_WARN_LED, LOW);
}

void run_gas_buzzer(const std_msgs::UInt16 toggle_buzzer) {
  if (toggle_buzzer.data == 0)
    noTone(BUZZER);
  else
    tone(BUZZER, toggle_buzzer.data);

  delay(1000);
}

void update_rServo(const std_msgs::UInt16 & angle) {
  rServo.write(angle.data);
}

void update_lServo(const std_msgs::UInt16 & angle) {
  lServo.write(angle.data);
}

ros::Subscriber<std_msgs::Bool> warning_Led("Gas_Warning_LEDs", toggle_warning_led);
ros::Subscriber<std_msgs::UInt16> gas_buzzer("Gas_Buzzer", run_gas_buzzer);

ros::Subscriber<std_msgs::UInt16>right_servo("Right_Ear_Controller", update_rServo);
ros::Subscriber<std_msgs::UInt16>left_servo("Left_Ear_Controller", update_lServo);


void setup()
{
  pinMode(BUZZER, OUTPUT);
  pinMode(GAS_WARN_LED, OUTPUT);

  rServo.attach(RIGHT_EAR);
  lServo.attach(LEFT_EAR);

  nh.initNode();

  nh.subscribe(warning_Led);
  nh.subscribe(gas_buzzer);
  
  nh.subscribe(right_servo);
  nh.subscribe(left_servo);
}


void loop()
{
  std_msgs::String gas_reads;

  // read from sensor and send gas reads as publisher
  
  nh.spinOnce();

  delay(1000);
}
