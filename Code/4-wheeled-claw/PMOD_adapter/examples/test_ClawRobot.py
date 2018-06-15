from ClawRobot import ClawRobot
import time

my_robot = ClawRobot(motors1_port='JC', motors2_port='JB', servos_port='JAB')

print('I am closing my claw')
my_robot.close_claw()
time.sleep(2)

print('I am opening my claw')
my_robot.open_claw()
time.sleep(2)

print('I am closing my claw')
my_robot.close_claw()
time.sleep(2)

print('I am going forward for 2 seconds')
my_robot.forward()
time.sleep(2)

print('I am going reverse for 2 seconds')
my_robot.reverse()
time.sleep(2)

print('I am going left for 2 seconds')
my_robot.left()
time.sleep(2)

print('I am going right for 2 seconds')
my_robot.right()
time.sleep(2)