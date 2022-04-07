#include <ros.h>
#include <ArduinoHardware.h>
#include <std_msgs/String.h>
#include <std_msgs/Bool.h>
#include <std_msgs/UInt16.h>
#include <Servo.h>


//********************** TESTING IN PROGRESS



// Setting the pins on board for


// Inputs (Sensors, Switches, etc.)
#define LIGHT_SENSOR_F A4
#define LIGHT_SENSOR_R A5

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

Servo rServo;
Servo lServo;


// Toggle LED light when the gas is detected
void toggle_co_led(const std_msgs::Bool & led_toggle)
{
  if (led_toggle.data == true)
    while (1) {
      digitalWrite(CO_WARN_LED, HIGH);
      delay(100);
      digitalWrite(CO_WARN_LED, LOW);
      delay(100);
    }
  else
    digitalWrite(CO_WARN_LED, LOW);
}

void toggle_prop_led(const std_msgs::Bool & led_toggle)
{
  if (led_toggle.data == true)
    while (1) {
      digitalWrite(PROP_WARN_LED, HIGH);
      delay(100);
      digitalWrite(PROP_WARN_LED, LOW);
      delay(100);
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


std_msgs::UInt16 light_val;
ros::Publisher front_light_sensor("Front_Light_Sensor", &light_val);
ros::Publisher back_light_sensor("Back_Light_Sensor", &light_val);

std_msgs::UInt16 gas_val;
ros::Publisher mq6_sensor("MQ6_Sensor", &gas_val);
ros::Publisher mq7_sensor("MQ7_Sensor", &gas_val);


ros::Subscriber<std_msgs::Bool> co_warning_Led("CO_Warning_LED", toggle_co_led);
ros::Subscriber<std_msgs::Bool> prop_warning_Led("Prop_Warning_LED", toggle_prop_led);

ros::Subscriber<std_msgs::UInt16> gas_buzzer("Gas_Buzzer", run_gas_buzzer);

ros::Subscriber<std_msgs::UInt16> right_servo("Right_Ear_Controller", update_rServo);
ros::Subscriber<std_msgs::UInt16> left_servo("Left_Ear_Controller", update_lServo);

ros::Subscriber<std_msgs::UInt16> blue_light("Update_Light_Lumens", update_outLight);


void setup()
{
  Serial.begin(57600);

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

  nh.initNode();

  nh.advertise(front_light_sensor);
  nh.advertise(back_light_sensor);

  nh.advertise(mq6_sensor);
  nh.advertise(mq7_sensor);

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
  light_v = analogRead(A4);
  light_val.data = light_v;
  front_light_sensor.publish(&light_val);

  light_v = analogRead(A5);
  light_val.data = light_v;
  back_light_sensor.publish(&light_val);

  gas_reads = analogRead(A0);
  gas_val.data = gas_reads;
  mq6_sensor.publish(&gas_val);

  gas_reads = analogRead(A1);
  gas_val.data = gas_reads;
  mq7_sensor.publish(&gas_val);

  delay(1000);


  nh.spinOnce();
}
