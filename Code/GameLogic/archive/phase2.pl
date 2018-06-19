
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

robot_is_at_center(
        RobotX, 
        RobotY, 
	RampMinX, 
	RampMaxX, 
	RampMinY, 
	RampMaxY
) :-
    robot_is_at_x_center(
        RobotX, 
	RampMinX, 
	RampMaxX),
    robot_is_at_y_center(
        RobotY,
        RampMinY,
	RampMaxY).

robot_is_at_x_center(RobotX, RampMinX, RampMaxX) :-
    RobotX > RampMinX,
    RobotX < RampMaxX.

robot_is_at_y_center(RobotY, RampMinY, RampMaxY) :-
    RobotY > RampMinY,
    RobotY < RampMaxY.

/* Robot is behind the ramp 
* if the robot's Y-postion is 
* greater than both the top left and right corners of the ramp */
robot_is_behind_ramp(RobotY, RampMaxY) :-
    RobotY > RampMaxY.
		
/* Robot is on the left-side of the ramp 
* if the robot's X-position is 
* lesser than the top and bottom left corners of the ramp */
robot_is_left_of_ramp(RobotX, RampMinX) :-
    RobotX < RampMinX.

/* Robot is on the right-side of the ramp 
* if the robot's X-position is 
* greater than the top and bottom right corners of the ramp */
robot_is_right_of_ramp(RobotX, RampMaxX) :-
    RobotX > RampMaxX.

/* Robot is in front of the ramp 
* if the robot's Y-position is 
* lesser than the bottom left and right corners of the ramp */
robot_is_in_front_of_ramp(RobotY, RampMinY) :-
    RobotY < RampMinY.

robot_is_behind_center_of_ramp(
        RobotX, 
        RobotY,
	RampMinX,
	RampMaxX,
	RampMinY,
	RampMaxY
) :-
    robot_is_behind_ramp(RobotY, RampMaxY),
    robot_is_at_x_center(RobotX, RampMinX, RampMaxX).

robot_is_front_center_of_ramp(
        RobotX, 
        RobotY,
	RampMinX,
	RampMaxX,
	RampMinY,
	RampMaxY
) :-
    robot_is_in_front_of_ramp(RobotY, RampMinY),
    robot_is_at_x_center(RobotX, RampMinX, RampMaxX).

robot_is_front_left_of_ramp(
        RobotX, 
        RobotY,
	RampMinX,
	RampMaxX,
	RampMinY,
	RampMaxY
) :-
    robot_is_in_front_of_ramp(RobotY, RampMinY),
    robot_is_left_of_ramp(RobotX, RampMinX).

robot_is_front_right_of_ramp(
        RobotX, 
        RobotY,
	RampMinX,
	RampMaxX,
	RampMinY,
	RampMaxY
) :-
    robot_is_in_front_of_ramp(RobotY, RampMinY),
    robot_is_right_of_ramp(RobotX, RampMaxX).


/* IF the robot's (x, y) position is 
* behind the ramp 
* AND to the center of the ramp, 
* THEN rotate 270 degrees east of the ramp */
rotate_270_degrees_west_of_ramp(
        RobotX, 
        RobotY, 
	RampMinX, 
	RampMaxX,
	RampMinY,	
	RampMaxY) :-
    robot_is_behind_center_of_ramp(
        RobotX,
        RobotY, 
        RampMinX, 
	RampMaxX,
	RampMinY,
        RampMaxY);
    robot_is_front_right_of_ramp(
        RobotX,
        RobotY, 
        RampMinX, 
	RampMaxX,
	RampMinY,
        RampMaxY).

/* IF the ROBOT's POSITION is 
* FRONT of the RAMP 
* AND to the LEFT of the RAMP, 
* THEN ROTATE 90 degrees east of the RAMP
*/
rotate_90_degrees_east_of_ramp(
        RobotX, 
	RobotY, 
	RampMinX,
        RampMaxX,	
	RampMinY, 
	RampMaxY
) :-
    robot_is_front_left_of_ramp(
        RobotX, 
	RobotY, 
	RampMinX,
        RampMaxX,	
	RampMinY, 
	RampMaxY).

/* IF the ROBOT's POSITION is 
*  NOT in FRONT of the RAMP
*  AND (LEFT of the RAMP
*       OR RIGHT of the RAMP)
*  THEN ROTATE 180 degrees south of the RAMP
*/		
rotate_180_degrees_south_of_ramp(
        RobotX, 
	RobotY, 
	RampMinX,
        RampMaxX,	
	RampMinY, 
	RampMaxY
) :-
    not(robot_is_in_front_of_ramp(
        RobotY, 
	RampMinY)),
    (robot_is_left_of_ramp(RobotX, RampMinX);
     robot_is_right_of_ramp(RobotX, RampMaxX)
    ).
/* IF the ROBOT's POSTION is
* FRONT and CENTER of the RAMP
* THEN ROTATE to 0 degrees north of the RAMP
*/
rotate_0_degrees_north_of_ramp(
        RobotX, 
	RobotY, 
	RampMinX,
        RampMaxX,	
	RampMinY, 
	RampMaxY

) :-
    robot_is_front_center_of_ramp(
        RobotX, 
        RobotY,
	RampMinX,
	RampMaxX,
	RampMinY,
	RampMaxY).

/* rule format:
* 	target(Position, Target).
*/
target(front_and_center, can).
target(front_and_left, front_and_center).
target(front_and_right, front_and_center).
target(center_and_left, front_and_left).
target(center_and_right, front_and_right).
target(back_and_left, front_and_left).
target(back_and_right, front_and_right).
target(back_and_center, back_and_left).

/* rule format:
* 	direction(Position, Orientation).
*/
direction(front_and_center, north).
direction(front_and_left, east).
direction(front_and_right, west).
direction(center_and_left, south).
direction(center_and_right, south).
direction(back_and_left, south).
direction(back_and_right, south).
direction(back_and_center, west).
