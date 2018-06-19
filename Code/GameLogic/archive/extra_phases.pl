below_ramp(Robot_Y, Ramp_Y) :-
			Robot_Y < Ramp_Y.

right_align_below(Robot_Theta, Ramp_Theta) :-
			Robot_Theta > Ramp_Theta + 10.
			
left_align_below(Robot_Theta, Ramp_Theta) :-
			Robot_Theta < Ramp_Theta - 10.
			
right_of_ramp(Robot_X, Ramp_X) :-
			Robot_X > Ramp_X.

left_of_ramp(Robot_X, Ramp_X) :-
			Robot_X < Ramp_X.
			
facing_right_of_ramp(Robot_Theta, Ramp_Theta) :-
			Robot_Theta < Ramp_Theta,
			Robot_Theta < 30,
			Robot_Theta > 330.

facing_left_of_ramp(Robot_Theta, Ramp_Theta) :-
			Robot_Theta > Ramp_Theta, 
			Robot_Theta < 210,
			Robot_Theta > 150.
			
above_ramp(Robot_Y, Ramp_Y) :-
			Robot_Y > Ramp_Y.
