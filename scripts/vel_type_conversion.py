#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist, TwistWithCovarianceStamped, Vector3Stamped
import argparse


#maps the joystick values and cmd_Vel
def map(val, in_min, in_max, out_min, out_max):
	return (val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def callback(data):
	msg = TwistWithCovarianceStamped()

	msg.header.seq = data.header.seq
	msg.header.stamp.secs = data.header.stamp.secs
	msg.header.stamp.nsecs = data.header.stamp.nsecs
	msg.header.frame_id = data.header.frame_id

	msg.twist.twist.linear.x = data.vector.x
	msg.twist.twist.linear.y = data.vector.y
	msg.twist.twist.linear.z = data.vector.z

	pub.publish(msg)


def start(NS):
	global pub

	if NS is None:
		ublox_fix_vel_topic = "/ublox/fix_velocity"
		ublox_fix_vel_temp_topic = "/ublox/fix_velocity_temp"
	else:
		if NS.startswith("/"):
			ublox_fix_vel_topic = NS + "/ublox/fix_velocity"
			ublox_fix_vel_temp_topic = NS + "/ublox/fix_velocity_temp"
		else:
			ublox_fix_vel_topic = "/" + NS + "/ublox/fix_velocity"
			ublox_fix_vel_temp_topic = "/" + NS + "/ublox/fix_velocity_temp"


	rospy.init_node('velocity_type_conversion_node', anonymous=True)
	pub = rospy.Publisher(ublox_fix_vel_topic, TwistWithCovarianceStamped)
	rospy.Subscriber(ublox_fix_vel_temp_topic, Vector3Stamped, callback)
	
	rospy.spin()

if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='convert velocity from Vector3Stamped to TwistWithCovarianceStamped')
	parser.add_argument('--ns',
						help="a namespace in front of topics")

	args = parser.parse_args(rospy.myargv()[1:])	# to make it work on launch file
	ns = args.ns

	if ns is not None:
		print("Use namespace as {:}".format(ns))
	else:
		print("No namespace, using default")

	start(ns)