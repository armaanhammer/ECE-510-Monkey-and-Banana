def update_claw(claw_to_can_distance, claw_to_can_angle, mySocket, move_robot=True):
    angle_buffer = 10
    max_distance = 75

    largest_angle = 360 - (angle_buffer/2)
    smallest_angle = (angle_buffer/2)

    if(bool(list(prolog.query("move_forward(claw_to_can_angle, claw_to_can_distance)")))):
		print('open')
        print('forward')
        if move_robot:
			send_command(mySocket, 'open')
            send_command(mySocket, 'forward')
    elif(bool(list(prolog.query("stop_and_close(claw_to_can_theta, claw_to_can_distance)")))):
		print('stop')
        print('close')
        if move_robot:
            send_command(mySocket, 'stop')
            send_command(mySocket, 'close')
    elif(bool(list(prolog.query("can_move_left(claw_to_can)")))):
		print('turn left')
        if move_robot:
            send_command(mySocket, 'left')
    else:
        print('turn right')
        if move_robot:
            send_command(mySocket, 'right')
