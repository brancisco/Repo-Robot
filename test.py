import serial
ser = serial.Serial('/dev/cu.ArcBotics-DevB', 9600)
# ser = serial.Serial('/dev/cu.Bluetooth-Incoming-Port', 9600)
import time
from time import sleep
import math

est_pose_x = 0 #set the previous known location here
est_pose_y = 0 #set the previous known location here
est_theta = 60 #set the previous known theta here

#Functions to control sparki
def move_forward():
	ser.write(b'1')

def move_backward():
	ser.write(b'2')

def move_right():
	ser.write(b'3')

def move_left():
	ser.write(b'4')

def move_stop():
	ser.write(b'5')

def open_grip():
	ser.write(b'6')

def close_grip():
	ser.write(b'7')

def follow_line():
	ser.write(b'8')

def repo():
	ser.write(b'9')

def turn_around():
	ser.write(b't')


def find_path():
	curr_x = 0
	curr_y = 0
	dest_x = 4
	dest_y = 1

	dx = dest_x - curr_x
	dy = dest_y - curr_y

	print("dX: ", dx,"dY: ", dy)

	if (dx < 0):
		move_left()
		sleep(0.01)
		move_forward()
		# dest = True

	if (dx > 0):
		move_right()
		dest = True
 
	if (dy < 0):  #turns Sparki around and then keeps going forward
		turn_around()
		sleep(5)
		move_stop()
		sleep(0.1)
		move_forward()
		# dest = True

	if (dy > 0):
		move_forward()
		# dest = True

	if ((dx == 0) and (dy == 0)):
		print("At the destination!")
		move_stop()
		# dest = False
		patrol = False
		sleep(0.1)
		repo()

def to_radians(deg):
	return deg * 3.14159/180

def to_degrees(rad):
	return rad * 180/3.14159

def updatePosition(est_pose_x, est_pose_y, est_theta):
	#Add if condition when we get the ArUco working
	robot_speed = 0.0278
	cycle_time = .100 
	axle_diameter = 0.0865
	pi = 3.14159
	left_speed_pct = 0
	right_speed_pct = 90
	
	left_wheel_rotating = 1
	right_wheel_rotating = 1

	est_pose_x += math.cos(to_radians(est_theta)) * \
	cycle_time * robot_speed * ((left_wheel_rotating * left_speed_pct) + \
	(right_wheel_rotating * right_speed_pct))/2
	est_pose_x = round(est_pose_x, 3)

	est_pose_y += math.sin(to_radians(est_theta)) * \
	cycle_time * robot_speed * ((left_wheel_rotating * left_speed_pct) + \
	(right_wheel_rotating * right_speed_pct))/2
	est_pose_y = round(est_pose_y, 3)

	est_theta += (((right_wheel_rotating * right_speed_pct) - \
	(left_wheel_rotating * left_speed_pct)) * cycle_time * robot_speed)/axle_diameter
	est_theta = round(est_theta, 3)

	print("Estimated Pose X: ", est_pose_x, "\n")
	print("Estimated Pose Y: ", est_pose_y, "\n")
	print("Estimated Theta: ", est_theta, "\n")


def main():
	
	while True:
		uin = input('enter in control\n')
		if uin == 'f':
			move_forward()
		elif uin == 'r':
			repo()
		elif uin == 'og':
			open_grip()
		elif uin == 's':
			move_stop()
		elif uin == 'l':
			follow_line()


if __name__ == '__main__':
	main()
