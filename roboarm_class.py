#!/usr/bin/python

import time, sys, traceback
import serial
from math import *


def translate(sensor_val, servo_low, servo_high):
	in_from = 0
	in_to = 180
	out_range =  servo_high - servo_low
	in_range = in_to - in_from
	in_val = sensor_val - in_from
	val=(float(in_val)/in_range)*out_range
	out_val = servo_low+val
	return str(int(out_val))

class roboarm_class():
	def __init__(self, com_port, baudrate):
		# serial port
		self.com_port = com_port
		self.baudrate = baudrate
		self.ser = serial.Serial(self.com_port, self.baudrate)
		#self.data = []
		self.x_degree = 0
		self.y_degree = 0
		self.dist = 0
		self.quality = 0
		self.rpm = 0
		self.clockwise = True
		#self.th = thread.start_new_thread(self.run, ())

	def move(self,move):
		if move == "straight_up":
			self.ser.write ('#1 P1300 #2 P1300 #3 P600 #4 P1630 T1500\r\n')
			time.sleep(1.6)
		if move == "inital_position_1":
			self.ser.write ('#0 P1750 #1 P1100 #2 P1100 #3 P1500 #4 P550 #5 P 1850 T1500\r\n')
			time.sleep(1.6)
		if move == "safety_position_1":
			self.ser.write ('#0 P1750 #1 P575 #2 P575 #3 P2050 #4 P1630 T1500\r\n')
			time.sleep(1.6)
	
	def hip(self, angle, ms):
		str_to_write = '#0 P' + translate(angle, 820, 2650) + ' T' + str(ms) + '\r\n'
		print str_to_write
		self.ser.write  (str_to_write)
		time.sleep((ms+200)/1000)

	def shoulder(self, angle, ms):
		str_to_write = '#1 P' + translate(angle, 525, 2075) + ' #2 P' + translate(angle,525, 2075) + ' T' + str(ms) + '\r\n'
		print str_to_write
		self.ser.write  (str_to_write)
		time.sleep((ms+200)/1000)	

	def elbow(self, angle, ms):
		str_to_write = '#3 P' + translate(angle, 560, 2100) + ' T' + str(ms) + '\r\n'
		print str_to_write
		self.ser.write  (str_to_write)
		time.sleep((ms+200)/1000)

	def wrist(self, angle, ms):
		str_to_write = '#4 P' + translate(angle, 750, 2500) + ' T' + str(ms) + '\r\n'
		print str_to_write
		self.ser.write  (str_to_write)
		time.sleep((ms+200)/1000)

	def grip(self, angle, ms):
		str_to_write = '#5 P' + translate(angle, 600, 2400) + ' T' + str(ms) + '\r\n'
		print str_to_write
		self.ser.write  (str_to_write)
		time.sleep((ms+200)/1000)

	def run(self):
		try:
			self.ser.close()
		except:
			pass
		while True:
			if (self.ser.isOpen() == False):
				self.ser = serial.Serial(self.com_port, self.baudrate)
				print "reconnecting serial port", self.com_port, self.baudrate
				self.ser = serial.Serial(self.com_port, self.baudrate)
				print self.ser
			time.sleep(0.001)

if __name__== "__main__":
	arm = roboarm_class('/dev/ttyUSB0', 115200)
	arm.move('safety_position_1')
	arm.wrist(180, 1000)
	arm.elbow(90, 1000)
	while True:
		time.sleep(2)
		arm.move('safety_position_1')
		arm.move('inital_position_1')
		arm.move('straight_up')
		arm.wrist(0, 1000)
		arm.wrist(180, 1000)
		arm.wrist(90, 1000)
		arm.grip(0, 1000)
		arm.grip(180, 1000)
		arm.move('inital_position_1')
		arm.hip(180, 1000)
		arm.hip(0, 2000)
		arm.wrist(180, 1000)
		arm.elbow(140, 1000)
		arm.shoulder(180, 2000)
		arm.shoulder(0, 2000)
		arm.elbow(0, 2000)
		arm.elbow(180, 2000)	
		arm.wrist(90, 1000)
		arm.move('safety_position_1')
	
