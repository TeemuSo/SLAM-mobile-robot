#!/usr/bin/env python

# RPi stuff
import PCA9685
import RPi.GPIO as GPIO
import sys
import odometry
import motor_control
#sys.path.insert(0, '/home/pi/KF')
import time

###############
# ROS stuff
###############
import rospy
from geometry_msgs.msg import Twist

def parse_coords(msg):
    # Parse velocity and angular components
    x_velocity = msg.linear.x
    angular_velocity = msg.angular.z

    # Move robot forward
    pwm.write(4, 0, x_velocity)
    pwm.write(5, 0, x_velocity)
    if angular_velocity == 1.0:
        pwm_servo.write(0, 0, x_velocity)
        rospy.loginfo('Driving straight with value: {}'
            .format(x_velocity))
    elif angular_velocity < 450 and angular_velocity > 250:
        pwm_servo.write(0, 0, angular_velocity)
        rospy.loginfo('Turning with value: {}'
            .format(angular_velocity))
    else:
        rospy.logwarn('Value out of limits! {}'.format(angular_velocity))


def init():
    rospy.loginfo('Initializing...')
    # Init ROS node
    rospy.init_node('robot_movement', anonymous=True)
    velocity_subscriber = rospy.Subscriber('/cmd_vel', Twist, queue_size=10, callback=parse_coords)
    
    # Spin the sh-- DJ
    rospy.spin()

###############
# RPi stuff
###############

# Init GPIO pins
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# Initiate PWM's
pwm = PCA9685.PWM()
pwm_servo = PCA9685.PWM()

pwm.frequency = 500
pwm_servo.frequency = 60
GPIO.setup([pwm.Motor0_A, 
    pwm.Motor0_B, 
    pwm.Motor1_A, 
    pwm.Motor1_B, 
    7], GPIO.OUT
)
GPIO.output(Motor0_A, GPIO.LOW)
GPIO.output(Motor0_B, GPIO.HIGH)
GPIO.output(Motor1_A, GPIO.LOW)
GPIO.output(Motor1_B, GPIO.HIGH)

# Set motors forward
motor = motor_control.Motor(4,5)
motor.set_motors_forward()
motor.motors_forward(1)
motor.stop_motors()

if __name__ == '__main__':
    init()
    if rospy.is_shutdown():
        rospy.loginfo('Shutting ROS node down...')
        pwm.write(4, 0, 0)
        pwm.write(5, 0, 0)
        pwm_servo.write(0, 0, 350)
