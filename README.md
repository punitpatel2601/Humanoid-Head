# Humanoid-Head
Non-verbal humanoid type communication project

<h3>Description</h3>
<p>
<br>The purpose of the Humanoid Robot project is to supply aid in confined or hazardous spaces, such as those encountered in Search & Rescue, cave exploration, etc. where it may be too risky for a human to work due to various hazards such as presence of dangerous gasses. </br>
<br>The project entails programming the logic to control the head, ears, and several attached sensors of the robot, as well as designs for any components or software systems that may be necessary to achieve this.</br>
<br>The final product should be able to process decisions such as when to use a flashlight, when to alert if a gas leak is detected, and be able to engage in basic non-verbal communication with a subject.</br>
</p>

<h1>How to Setup</h1>
<br>To Set up the project, follow the circuit diagram provided in the User Document and connect the Respective sensors and outputs to their respective pins.</br>

        Attach light sensor on A4
        Attach light sensor on A5

        Attach MQ6_SENSOR at A0
        Attach MQ7_SENSOR at A1

        Attach the buzzer to pin number 11
        Attach the warning led to pin number 13
        Attach the warning led to pin number 12

        Attach Right ear Servo to pin 5
        Attach Left ear Servo to pin 6

        Attach blue output light to pin 8



<h1>How to Run</h1>
<p>
<h3>Pre-Requisites</h3>
1. Have installed ArduinoIDE. Follow -> "https://www.arduino.cc/en/software"
2. Have ROS Rosserial installed with all of its dependancies. Follow -> "http://wiki.ros.org/ROS/Installation"
3. Have a Ubuntu Machine (Can be a VM).
</p>

<p>
Loading the Program on Arduino:

1. Attach the Arduino UNO to the system. 
2. Open the Sketch under "arduino_sketch/Arduino/humanoid_head_sketch.ino" in the Arduino IDE. Load the sketch to the Arduino board. 
3. Note the port at which Arduino is connected. For example: "/dev/ttyACM0"
</p>

<p>
Open a terminal and navigate to "ros_ws" directory and the start ROS service:
        >> roscore

<p>
Connecting to the Arduino:

Open a new terminal and follow the steps belows to connect your Arduino UNO board to ROS.
        >> source devel/setup.bash
        >> sudo chmod 666 /dev/ttyACM0
        >> rosrun rosserial_python serial_node.py /dev/ttyACM0

Note: '/dev/ttyACM0' can be different if your Arduino is connected to different port.
</p>

<p>
<h4>Run any module indiviually</h4>

Open a new terminal for every service. 
        >> source devel/setup.bash
        >> rosrun "name_of_the_package" "name_of_the_module"

(below is an example for running "gas_detection_node")
        >> source devel/setup.bash
        >> rosrun gas_monitoring gas_detection_node.py
</p>

<p>
Description of each module (file):

1. gas_detection_node.py - Detects the Gas by looking at the data obtained from Robot.
2. gas_monitoring_node.py - Detects and Displays the Gas detected
3. front_light_node.py - Detects the Current ambient light setting and Then updates the output light.
4. ear_pos_control_station.py - Sets the emotion by controlling the ears, set by manual operator.
5. ear_servo_control_node.py  - Checks all the emotions from different packages, set the most prioritized emotion.
</p>