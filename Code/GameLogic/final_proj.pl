/* 
	Matt Fleetwood
	ECE 410/510
	Monkey and Banana Prolog Planner module
	
	This program provides the next action for the robot to perform (move left, right, forward, backward).
	Inputs into the module are (x, y) coordinates of the robot and the goal object.
	Outputs are the commands for the robot to perform as described above.
*/

atGoal(RobotX, RobotY, GoalObjectX, GoalObjectY) :-
		RobotX is GoalObjectX,
		RobotY is GoalObjectY.

moveWest(RobotX, RobotTheta, GoalObjectX) :-
		RobotX > GoalObjectX,
		RobotTheta is 90.
		
moveWest(RobotX, RobotTheta, GoalObjectX) :-
		RobotX > GoalObjectX, 
		RobotTheta is 270. 
		
moveEast(RobotX, RobotTheta, GoalObjectX) :-
		RobotX < GoalObjectX,
		RobotTheta is 90.
		
moveEast(RobotX, RobotTheta, GoalObjectX) :-
		RobotX < GoalObjectX, 
		RobotTheta is 270. 
		
moveNorth(RobotY, RobotTheta, GoalObjectY) :-
		RobotY < GoalObjectY,
		RobotTheta is 90.
		
moveSouth(RobotY, RobotTheta, GoalObjectY) :-
		RobotY > GoalObjectY, 
		RobotTheta is 270. 
