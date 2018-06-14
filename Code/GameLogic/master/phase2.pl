
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

robot_is_at_center(RobotX, RobotY, RampTopLeftCornerX, RampBotLeftCornerX, RampTopRightCornerX, RampBotRightCornerX, 
					RampTopLeftCornerY, RampBotLeftCornerY, RampTopRightCornerY, RampBotRightCornerY) :-
		RobotX > RampBotLeftCornerX,
		RobotX > RampTopLeftCornerX, 
		RobotX < RampBotRightCornerX,
		RobotX < RampTopRightCornerX,
		RobotY > RampBotLeftCornerY,
		RobotY > RampBotRightCornerY,
		RobotY < RampTopLeftCornerY,
		RobotY < RampTopRightCornerY.

/* Robot is behind the ramp if the robot's Y-postion is greater than both the top left and right corners of the ramp */
robot_is_behind_ramp(RobotY, RampTopLeftCornerY, RampTopRightCornerY) :-
		RobotY > RampLeftCornerY,
		RobotY > RampRightCornerY.
		
/* Robot is on the left-side of the ramp if the robot's X-position is lesser than the top and bottom left corners of the ramp */
robot_is_left_of_ramp(RobotX, RampTopLeftCornerX, RampBotLeftCornerX) :-
		RobotX < RampTopLeftCornerX,
		RobotX < RampBotLeftCornerX.

/* Robot is on the right-side of the ramp if the robot's X-position is greater than the top and bottom right corners of the ramp */
robot_is_right_of_ramp(RobotX, RampTopRightCornerX, RampBotRightCornerX) :-
		RobotX > RampTopLeftCornerX,
		RobotX > RampBotLeftCornerX.

/* Robot is in front of the ramp if the robot's Y-position is lesser than the bottom left and right corners of the ramp */
robot_is_in_front_of_ramp(RobotY, RampBotLeftCornerY, RampBotRightCornerY) :-
		RobotY < RampLeftCornerY,
		RobotY < RampRightCornerY.

/* IF the robot's (x, y) position is behind the ramp AND to the left of the ramp, THEN rotate 270 degrees east of the ramp */
rotate_270_degrees_east_of_ramp(RobotX, RobotY, RampTopLeftCornerX, RampBotLeftCornerX, RampTopLeftCornerY, RampTopRightCornerY) :-
		robot_is_behind_ramp(RobotY, RampTopLeftCornerY, RampTopRightCornerY),
		robot_is_left_of_ramp(RobotX, RampTopLeftCornerX, RampBotLeftCornerX).

/* IF the robot's (x, y) position is behind the ramp AND to the right of the ramp, THEN rotate 90 degrees west of the ramp */
rotate_90_degrees_west_of_ramp(RobotX, RobotY, RampTopLeftCornerY, RampTopRightCornerY, RampTopRightCornerX, RampBotRightCornerX) :-
		robot_is_behind_ramp(RobotY, RampTopLeftCornerY, RampTopRightCornerY),
		robot_is_right_of_ramp(RobotX, RampTopRightCornerX, RampBotRightCornerX.

/* IF the robot's (x, y) position is NOT in front of the ramp, THEN rotate 180 degrees south of the ramp*/		
rotate_180_degrees_south_of_ramp(RobotY, RampBotLeftCornerY, RampBotRightCornerY) :-
		not(robot_is_in_front_of_ramp(RobotY, RampBotLeftCornerY, RampBotRightCornerY)).

/* IF robot's (x, y) position is in front of the ramp AND to the left of the ramp, THEN rotate 90 degrees of the ramp and move to the center of the ramp */
rotate_90_degrees_and_move_to_center(RobotX, RobotY, RampTopLeftCornerX, RampBotLeftCornerX, RampBotLeftCornerY, RampBotRightCornerY) :-
		robot_is_in_front_of_ramp(RobotY, RampBotLeftCornerY, RampBotRightCornerY),
		robot_is_left_of_ramp(RobotX, RampTopLeftCornerX, RampBotLeftCornerX).

/* IF robot's (x, y) position is in front of the ramp AND to the right of the ramp, THEN rotate 270 degrees of the ramp and move to the center of the ramp*/		
rotate_270_degrees_and_move_to_center(RobotX, RobotY, RampBotLeftCornerY, RampBotRightCornerY, RampTopRightCornerX, RampBotRightCornerX) :-
		robot_is_in_front_of_ramp(RobotY, RampBotLeftCornerY, RampBotRightCornerY),
		robot_is_right_of_ramp(RobotX, RampTopRightCornerX, RampBotRightCornerX).

/* IF robot's (x, y) position is in front of the ramp AND in the center, THEN rotate 0 degrees of the ramp and retrieve the can */		
rotate_0_degrees_and_retrieve_can(RobotX, RobotY, RampTopLeftCornerX, RampBotLeftCornerX, RampTopRightCornerX, RampBotRightCornerX, 
					RampTopLeftCornerY, RampBotLeftCornerY, RampTopRightCornerY, RampBotRightCornerY ) :-
		robot_is_in_front_of_ramp(RobotY, RampBotLeftCornerY, RampBotRightCornerY),
		robot_is_at_center(RobotX, RobotY, RampTopLeftCornerX, RampBotLeftCornerX, RampTopRightCornerX, RampBotRightCornerX, 
					RampTopLeftCornerY, RampBotLeftCornerY, RampTopRightCornerY, RampBotRightCornerY).
