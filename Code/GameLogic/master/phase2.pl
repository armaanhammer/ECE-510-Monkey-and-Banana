/*
	Matt Fleetwood
	ECE 410/510
	Final Project: Phase 2 Prolog Program
	6/14/2018
	
	This program uses Prolog rules for Python to determine where the robot should go next. Inputs from Python are (x, y) 
  coordinates of the robot and the Cartesian coordinates for the left, right, front, and back of the ramp.
	Coordinates are defined by the Aruco markers. The robot uses one marker while the ramp uses four (two for the top and
  bottom corners).
*/

robot_is_behind_ramp(RobotY, RampTopLeftCornerY, RampTopRightCornerY) :-
		RobotY > RampLeftCornerY,
		RobotY > RampRightCornerY.

robot_is_left_of_ramp(RobotX, RampTopLeftCornerX, RampBotLeftCornerX) :-
		RobotX < RampTopLeftCornerX,
		RobotX < RampBotLeftCornerX.
		
robot_is_right_of_ramp(RobotX, RampTopRightCornerX, RampBotRightCornerX) :-
		RobotX > RampTopLeftCornerX,
		RobotX > RampBotLeftCornerX.

robot_is_in_front_of_ramp(RobotY, RampBotLeftCornerY, RampBotRightCornerY) :-
		RobotY < RampLeftCornerY,
		RobotY < RampRightCornerY.
