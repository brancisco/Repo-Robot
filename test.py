import FingerCounter

import serial
ser = serial.Serial('/dev/cu.usbmodem14201', 9600)
# ser = serial.Serial('/dev/cu.Bluetooth-Incoming-Port', 9600)
import time
from time import sleep
import math

# est_pose_x = 0 #set the previous known location here
# est_pose_y = 0 #set the previous known location here
# est_theta = 0 #set the previous known theta here
# left_wheel_rotating = 1
# right_wheel_rotating = 1
# robot_speed = 0.0278
# cycle_time = .100 
# axle_diameter = 0.0865
# pi = 3.14159
# left_speed_pct = 1
# right_speed_pct = 1

#Functions to control sparki
def move_stop():
	# global left_wheel_rotating
	# global right_wheel_rotating
	# global left_speed_pct
	# global right_speed_pct
	ser.write(b'0')
	# left_wheel_rotating = 0
	# right_wheel_rotating = 0
	# left_speed_pct = 0
	# right_speed_pct = 0
def move_forward():
	# global left_wheel_rotating
	# global right_wheel_rotating
	ser.write(b'1')
	# left_wheel_rotating = 1
	# right_wheel_rotating = 1

def move_backward():
	# global left_wheel_rotating
	# global right_wheel_rotating
	ser.write(b'2')

def move_right():
	# global left_wheel_rotating
	# global right_wheel_rotating
	ser.write(b'3')
	# left_wheel_rotating = 1
	# right_wheel_rotating = 0

# def move_left():
# 	global left_wheel_rotating
# 	global right_wheel_rotating
# 	ser.write(b'4')
# 	left_wheel_rotating = 0
# 	right_wheel_rotating = 1

def open_grip():
	ser.write(b'4')

def close_grip():
	ser.write(b'5')

# def follow_line():
# 	ser.write(b'8')

# def repo():
# 	ser.write(b'9')

# def turn_around():
# 	ser.write(b't')


# def find_path():
# 	curr_x = 0
# 	curr_y = 0
# 	dest_x = 4
# 	dest_y = 1

# 	dx = dest_x - curr_x
# 	dy = dest_y - curr_y

# 	print("dX: ", dx,"dY: ", dy)

# 	if (dx < 0):
# 		move_left()
# 		sleep(0.01)
# 		move_forward()
# 		# dest = True

# 	if (dx > 0):
# 		move_right()
# 		dest = True
 
# 	if (dy < 0):  #turns Sparki around and then keeps going forward
# 		turn_around()
# 		sleep(5)
# 		move_stop()
# 		sleep(0.1)
# 		move_forward()
# 		# dest = True

# 	if (dy > 0):
# 		move_forward()
# 		# dest = True

# 	if ((dx == 0) and (dy == 0)):
# 		print("At the destination!")
# 		move_stop()
# 		# dest = False
# 		patrol = False
# 		sleep(0.1)
# 		repo()

# def to_radians(deg):
# 	return deg * 3.14159/180

# def to_degrees(rad):
# 	return rad * 180/3.14159

# def updatePosition():
# 	#Add if condition when we get the ArUco working

# 	global est_pose_x
# 	global est_pose_y
# 	global est_theta
# 	global left_wheel_rotating
# 	global right_wheel_rotating
# 	global right_speed_pct
# 	global left_speed_pct
# 	global robot_speed
# 	global cycle_time
# 	global axle_diameter


# 	est_pose_x += math.cos(to_radians(est_theta)) * \
# 	cycle_time * robot_speed * ((left_wheel_rotating * left_speed_pct) + \
# 	(right_wheel_rotating * right_speed_pct))/2
# 	est_pose_x = round(est_pose_x, 3)

# 	est_pose_y += math.sin(to_radians(est_theta)) * \
# 	cycle_time * robot_speed * ((left_wheel_rotating * left_speed_pct) + \
# 	(right_wheel_rotating * right_speed_pct))/2
# 	est_pose_y = round(est_pose_y, 3)

# 	est_theta += (((right_wheel_rotating * right_speed_pct) - \
# 	(left_wheel_rotating * left_speed_pct)) * cycle_time * robot_speed)/axle_diameter
# 	est_theta = round(est_theta, 3)

# 	print("Pose X: ", est_pose_x, end=' ')
# 	print("Pose Y: ", est_pose_y, end=' ')
# 	print("Pose T: ", est_theta, '\r', end='')
def get_state(img):
	state = str[count_fingers(img)]
	# uin = input('enter in control: \n')
	if state == '0':
		move_stop()
	elif state == '1':
		move_forward()
	elif state == '2':
		move_backward()
	elif state == '3':
		move_right()
	elif state == '4':
		close_grip()
	elif state == '5':
		open_grip()


def main():

	stream_to_program_mac(get_state)
	# while True:
	
		

if __name__ == '__main__':
	main()
