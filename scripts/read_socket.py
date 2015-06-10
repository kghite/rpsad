"""
Edited: 6/10/15
Description: Universal node for getting module data from RPi sockets
"""

#!/usr/bin/env python
import rospy
from std_msgs.msg import *
from geometry_msgs.msg import *
from sensor_msgs.msg import *
import socket
import sys
import time

# ROS publisher setup
rospy.init_node("read_socket")
PORT = rospy.get_param('~PORT')
MESSAGE = rospy.get_param('~MESSAGE')

# PROBLEM: The MESSAGE is coming in as "String" rather than String
module_pub = rospy.Publisher('test_string', MESSAGE, queue_size=10)

# Socket setup
HOST = '192.168.32.231'
#PORT = 8888
buffer = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket Created'
s.connect((HOST, PORT))

# Get and publish socket data
stream_start = 'BEGIN_MESSAGE'
stream_end = 'END_MESSAGE'
data_stream = ''
start_time = time.time()
while True:
	try:
		data = s.recv(1024)
		if not data:
			break
		data_stream += data
		if data_stream.find(stream_end) != -1:
			# Cut full message from stream
			msg_index = data_stream.find(stream_start) + len(stream_start)
			msg_end = data_stream.find(stream_end)
			raw_msg = data_stream[msg_index : msg_end]
			# Get the time stamp
			time_stamp = time.time() - start_time
			# Format data as a ROS message and publish
			message = raw_msg + str(time_stamp)
			print message
			module_pub.publish(message)
	except socket.error, msg:
		sys.stderr.write('Error: %s\n' % msg)
		print 'Disconnected'
		break