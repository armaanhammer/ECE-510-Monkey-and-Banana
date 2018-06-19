
/*
	Matt Fleetwood / David Hernandez
	ECE 410/510
	Final Project: Phase 2.1 Prolog Program
	6/17/2018
	
	This program uses Prolog rules for Python to determine where the robot should go next. Inputs from Python are (x, y) 
	coordinates of the Robot and Goal.
	Coordinates are defined by the Aruco markers. The robot uses one marker while the Goal is calculated from 
'world' markers which uses four ID's (two for the top and
	bottom corners). Note Top of screen is North heading in +Y direction.
*/

robot_is_at_center(
        RobotX, 
        RobotY, 
	GoalX, 
	GoalY
) :-
    robot_is_at_x_center(
        RobotX, 
	GoalX),
    robot_is_at_y_center(
        RobotY,
        GoalY).

robot_is_at_x_center(RobotX, GoalX) :-
    RobotX == GoalX.

robot_is_at_y_center(RobotY, GoalY) :-
    RobotY == GoalY.

/* Robot is North of the Goal 
* if the robot's Y-postion is 
* greater than goal's Y-position */
robot_is_north_goal(RobotY, GoalY) :-
    RobotY > GoalY.
		
/* Robot is on the west-side of the goal 
* if the robot's X-position is 
* lesser than the goal's X-position */
robot_is_west_of_goal(RobotX, GoalX) :-
    RobotX < GoalX.

/* Robot is on the east-side of the goal 
* if the robot's X-position is 
* greater than goal's X-position */
robot_is_east_of_goal(RobotX, GoalX) :-
    RobotX > GoalX.

/* Robot is south of the goal 
* if the robot's Y-position is 
* lesser than the goal's Y-position */
robot_is_south_of_goal(RobotY, GoalY) :-
    RobotY < GoalY.

robot_is_north_center_of_goal(
        RobotX, 
        RobotY,
	GoalX,
	GoalY
) :-
    robot_is_north_goal(RobotY, GoalY),
    robot_is_at_x_center(RobotX, GoalX).

robot_is_south_center_of_goal(
        RobotX, 
        RobotY,
	GoalX,
	GoalY
) :-
    robot_is_south_of_goal(RobotY, GoalY),
    robot_is_at_x_center(RobotX, GoalX).


/* IF the robot's (x, y) position is 
* north the goal 
* AND to the center of the goal, 
* THEN rotate 270 degrees east of the goal */
rotate_270_degrees_west_of_goal(
        RobotX, 
        RobotY, 
	GoalX, 
	GoalY) :-
    robot_is_north_center_of_goal(
        RobotX,
        RobotY, 
        GoalX, 
	GoalY);
    robot_is_south_east_of_goal(
        RobotX,
        RobotY, 
        GoalX, 
	GoalY).

/* IF the ROBOT's POSITION is 
* south of the goal 
* AND to the west of the goal, 
* THEN ROTATE 90 degrees east of the goal
*/
rotate_90_degrees_east_of_goal(
        RobotX, 
	RobotY, 
	GoalX,
        GoalY
) :-
    robot_is_south_west_of_goal(
        RobotX, 
	RobotY, 
	GoalX,
        GoalY).

/* IF the ROBOT's POSITION is 
*  NOT in south of the goal
*  AND (west of the goal
*       OR east of the RAMP)
*  THEN ROTATE 180 degrees south of the RAMP
*/		
rotate_180_degrees_south_of_goal(
        RobotX, 
	RobotY, 
	GoalX,
        GoalY
) :-
    not(robot_is_south_of_goal(
        RobotY, 
	GoalMinY)),
    (robot_is_west_of_goal(RobotX, GoalX);
     robot_is_east_of_goal(RobotX, GoalX)
    ).
/* IF the ROBOT's POSTION is
* FRONT and CENTER of the RAMP
* THEN ROTATE to 0 degrees north of the RAMP
*/
rotate_0_degrees_north_of_goal(
        RobotX, 
	RobotY, 
	GoalX,
        GoalY

) :-
    robot_is_south_center_of_goal(
        RobotX, 
        RobotY,
	GoalX,
	GoalY).

/* rule format:
* 	target(Position, Target).
*/
target(south_and_center, can).
target(south_and_west, south_and_center).
target(south_and_east, south_and_center).
target(center_and_west, south_and_west).
target(center_and_east, south_and_east).
target(back_and_west, south_and_west).
target(back_and_east, south_and_east).
target(back_and_center, back_and_west).

/* rule format:
* 	direction(Position, Orientation).
*/
direction(south_and_center, north).
direction(south_and_west, east).
direction(south_and_east, west).
direction(center_and_west, south).
direction(center_and_east, south).
direction(back_and_west, south).
direction(back_and_east, south).
direction(back_and_center, west).
