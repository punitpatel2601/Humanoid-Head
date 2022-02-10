#include <ros.h>
#include <std_msgs/UInt16.h>
#include <Servo.h>


#define RIGHT_EAR 5 //Attach Right ear Servo to pin 5
#define LEFT_EAR 6  //Attach Left ear Servo to pin 6


ros::NodeHandle nh;

Servo rServo; Servo lServo;

void update_rServo(const std_msgs::UInt16 & angle) {
  rServo.write(angle.data);
}

void update_lServo(const std_msgs::UInt16 & angle) {
  lServo.write(angle.data);
}

ros::Subscriber<std_msgs::UInt16>right_servo("Right_Ear_Controller", update_rServo);
ros::Subscriber<std_msgs::UInt16>left_servo("Left_Ear_Controller", update_lServo);


void setup() {
  rServo.attach(RIGHT_EAR);
  lServo.attach(LEFT_EAR);

  nh.initNode();

  nh.subscribe(right_servo);
  nh.subscribe(left_servo);
}

void loop() {
  nh.spinOnce();
  delay(2000);
}
