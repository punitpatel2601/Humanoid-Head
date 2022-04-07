#include <ros.h>
#include <ArduinoHardware.h>
#include <std_msgs/String.h>
#include <std_msgs/Bool.h>
#include <std_msgs/UInt16.h>
#include <Servo.h>


//********************** TESTING IN PROGRESS



// Setting the pins on board for


// Inputs (Sensors, Switches, etc.)
#define MQ6_SENSOR A0
#define MQ7_SENSOR A1

// Outputs (LEDs, Motors, Sounds, etc.)
#define BUZZER 11    //Attach the buzzer to pin number 11

#define PROP_WARN_LED 13 //Attach the warning led to pin number 13
#define CO_WARN_LED 12  //Attach the warning led to pin number 12

#define RIGHT_EAR 5 //Attach Right ear Servo to pin 5
#define LEFT_EAR 6  //Attach Left ear Servo to pin 6

#define BLUE_LIGHT 9 //Attach blue output light to pin 8

// global variables
ros::NodeHandle nh;
std_msgs::String gas_reading;

Servo rServo;
Servo lServo;


// Toggle LED light when the gas is detected
void toggle_co_led(const std_msgs::Bool & led_toggle)
{
  if (led_toggle.data == true)
    while(1) {
      digitalWrite(CO_WARN_LED, HIGH);
      delay(100);
      digitalWrite(CO_WARN_LED, LOW);
    }
  else
    digitalWrite(CO_WARN_LED, LOW);
}

void toggle_prop_led(const std_msgs::Bool & led_toggle)
{
  if (led_toggle.data == true)
    while(1) {
      digitalWrite(PROP_WARN_LED, HIGH);
      delay(100);
      digitalWrite(PROP_WARN_LED, LOW);
    }
  else
    digitalWrite(PROP_WARN_LED, LOW);
}

void run_gas_buzzer(const std_msgs::UInt16 & toggle_buzzer) {
  if (toggle_buzzer.data != 0)
    analogWrite(BUZZER, toggle_buzzer.data);
  else
    analogWrite(BUZZER, 0);

  delay(1000);
}

void update_rServo(const std_msgs::UInt16 & angle) {
  rServo.write(angle.data);
}

void update_lServo(const std_msgs::UInt16 & angle) {
  lServo.write(angle.data);
}

void update_outLight(const std_msgs::UInt16 & lumens) {
  analogWrite(BLUE_LIGHT, lumens.data);
  delay(100);
}


ros::Subscriber<std_msgs::Bool> co_warning_Led("CO_Warning_LED", toggle_co_led);
ros::Subscriber<std_msgs::Bool> prop_warning_Led("Prop_Warning_LED", toggle_prop_led);


ros::Subscriber<std_msgs::UInt16> gas_buzzer("Gas_Buzzer", run_gas_buzzer);

ros::Subscriber<std_msgs::UInt16> right_servo("Right_Ear_Controller", update_rServo);
ros::Subscriber<std_msgs::UInt16> left_servo("Left_Ear_Controller", update_lServo);

ros::Subscriber<std_msgs::UInt16> blue_light("Update_Light_Lumens", update_outLight);


void setup()
{
  Serial.begin(57600);

  pinMode(MQ6_SENSOR, INPUT);
  pinMode(MQ7_SENSOR, INPUT);

  pinMode(BUZZER, OUTPUT);
  
  pinMode(CO_WARN_LED, OUTPUT);
  pinMode(PROP_WARN_LED, OUTPUT);

  pinMode(BLUE_LIGHT, OUTPUT);

  rServo.attach(RIGHT_EAR);
  lServo.attach(LEFT_EAR);

  nh.initNode();

  nh.subscribe(co_warning_Led);
  nh.subscribe(prop_warning_Led);
  
  nh.subscribe(gas_buzzer);

  nh.subscribe(right_servo);
  nh.subscribe(left_servo);

  nh.subscribe(blue_light);
}

int gas_sensor;

void loop()
{
  std_msgs::String gas_reads;

  delay(1000);


  nh.spinOnce();
}
