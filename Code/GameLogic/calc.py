"""
Matt Fleetwood
ECE 410/510
Spring 2018
Portland, OR

Function for calculating the angle difference and (x, y) distance between the robot and some goal 
object.

Inputs: robot's angle, (x,y) coordinates of robot, goal's angle, (x,y) coordinates of goal position
robot_info contains the first 3 args above, goal_info contains the last 3
For instance: robot_info[0] is the robot's angle;
			   robot_info[1] is the robot's x position
			   robot_info[2] is the robot's y position
The goal_info list is defined similarly to robot_info
Returns the angle difference between the 2 angles and the (x, y) distance between the two pairs of 
coordinates
"""

import math

def getAngleAndDist(robot_info, goal_info):
    """
    Example call: robo_ls = [90, 5, 5], goal_ls = [180, 0, 0]
                  (ang, dist) = getAngleAndDist(robo_ls, goal_ls)
                  
    This means ang (the difference between 180 and 90) is 90, 
    and dist (the distance between the pair of (x, y) coords) is 7.07
    
    """
	#Error check to see if we are missing information
    if(len(robot_info) != 3 or len(goal_info) != 3):
        print('Error: not enough information or info format not as expected')
        return
    angle_diff = goal_info[0] - robot_info[0] #Find difference between robot and goal angles
    x_diff = abs(goal_info[1] - robot_info[1]) #Get the differences between x and y coordinates
    y_diff = abs(goal_info[2] - robot_info[2])
    x_sq = math.pow(x_diff, 2) #Apply the rest of the distance formula
    y_sq = math.pow(y_diff, 2)
    x_y_diff = x_sq + y_sq
    return (angle_diff, math.sqrt(x_y_diff)) 
