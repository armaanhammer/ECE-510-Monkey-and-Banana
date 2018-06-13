/* 
	Matt Fleetwood
	ECE 410/510
	Monkey and Banana Prolog Planner module
	
	This program provides the next action for the robot to perform (move left, right, forward, backward).
	Inputs into the module are (x, y) coordinates of the robot and the goal object.
	Outputs are the commands for the robot to perform as described above.
*/


stop_and_close(Claw_to_can_theta, Claw_to_can_distance, Max_angle, Min_angle, Max_distance) :-
/* move_forward_and_open(Claw_to_can_theta, Claw_to_can_distance, Max_angle, Min_angle, Max_distance) :- */
			(Claw_to_can_theta > Max_angle; Claw_to_can_theta < Min_angle),
			Claw_to_can_distance < Max_distance.

move_forward_and_open(Claw_to_can_theta, Claw_to_can_distance, Max_angle, Min_angle, Max_distance) :-
/* stop_and_close(Claw_to_can_theta, Claw_to_can_distance, Max_angle, Min_angle, Max_distance) :- */
			(Claw_to_can_theta > Max_angle; Claw_to_can_theta < Min_angle),
			Claw_to_can_distance > Max_distance.

/*			
# move_forward_and_open(Claw_to_can_theta, Claw_to_can_distance, Max_angle, Min_angle, Max_distance) :-
# 			Claw_to_can_theta < Min_angle,
# 			Claw_to_can_distance > Max_angle.

			
# stop_and_close(Claw_to_can_theta, Claw_to_can_distance, Max_angle, Min_angle, Max_distance) :-
# 			Claw_to_can_theta < Min_angle, 
# 			Claw_to_can_distance < Max_distance.
*/

can_move_left(Claw_to_can, Threshold_angle) :-
			Claw_to_can > Threshold_angle.
			
/*
Sample query: Can we move forward for theta = 356 and distance = 76?
			 ?- move_forward_and_open(356, 76).
			 true.

*/
