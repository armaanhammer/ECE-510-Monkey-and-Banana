/* 
	Matt Fleetwood
	ECE 410/510
	Monkey and Banana Prolog Planner module
	
	This program provides the next action for the robot to perform (move left, right, forward, backward).
	Inputs into the module are (x, y) coordinates of the robot and the goal object.
	Outputs are the commands for the robot to perform as described above.
*/


/* stop(Claw_to_goal_theta, Claw_to_goal_distance, Max_angle, Min_angle, Max_distance) :-
 *			(Claw_to_goal_theta > Max_angle; Claw_to_goal_theta < Min_angle),
 *			Claw_to_goal_distance < Max_distance.
 */

stop(Claw_to_goal_distance, Max_distance) :-
			Claw_to_goal_distance < Max_distance.

forward(Claw_to_goal_theta, Claw_to_goal_distance, Max_angle, Min_angle, Max_distance) :-
			(Claw_to_goal_theta > Max_angle; Claw_to_goal_theta < Min_angle),
			Claw_to_goal_distance > Max_distance.

left(Claw_to_goal_theta, Threshold_angle) :-
			Claw_to_goal_theta > Threshold_angle.

/* rule format:
* 	target(Position, Target).
*/
target(center, can).
target(bottom_center, can).
target(bottom_left, bottom_center).
target(bottom_right, bottom_center).
target(center_left, bottom_left).
target(center_right, bottom_right).
target(top_left, center_left).
target(top_right, center_right).
target(top_center, top_left).			
			
/*
Sample query: Can we move forward for theta = 356 and distance = 76?
			 ?- forward(356, 76).
			 true.

*/
