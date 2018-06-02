import argparse
import socket
import time
#import yaml

from ClawRobot import ClawRobot
 
def get_args():
    parser = argparse.ArgumentParser(description='clawrobot server.')

    parser.add_argument(
            '--host',
            default='192.168.0.104',
            help='host ip of the clawrobot')

    parser.add_argument(
            '--port',
            default=5001,
            type=int,
            help='port used to communicate to the clawrobot')

    # parser.add_argument(
            # '-c',
            # '--config_file',
            # default='config_12DOF.yaml',
            # help='clawrobot configuration file')
    
    return parser.parse_args()

#def initialize_clawrobot(config_file):
def initialize_clawrobot():
    my_clawrobot = ClawRobot(motors1_port='JC', motors2_port='JB', servos_port='JAB')
    
    # # open config file
    # with open(config_file) as f:
        # my_config = yaml.load(f)

    # if config_file == 'config_12DOF.yaml':
        # my_clawrobot = clawrobot_12DOF(my_config)
        # my_clawrobot.initial_tests()
        
    # elif config_file == 'config_18DOF.yaml':
        # my_clawrobot = clawrobot_18DOF(my_config)
        # my_clawrobot.initial_tests()
        
    # else:
        # print('ERROR: Cannot recognize the config file!!!')

    return my_clawrobot


def command_processor(data, my_clawrobot):
    print('Data: {}'.format(data))

    items = data.split()
    if len(items) == 1:
        command = items[0]
        iteration = 1

    elif len(items) == 2:
        command = items[0]
        iteration = int(items[1])

    else:
        return 'ERROR: invalid command format'

    print('Command: {}'.format(command))
    print('Iteration: {}'.format(iteration))

    commands = [
        'open',
        'close',
        'left',
        'right',
        'forward',
        'go',
        'backward',
        'reverse',
        'test',
    ]
    
    if command == 'open':
        print('Opening claw...')
        my_clawrobot.open_claw()
        return ('Opened claw')

    elif command == 'close':
        print('Closing claw...')
        my_clawrobot.close_claw()
        return ('Closed claw')

    elif command == 'test':
        print('test')
        return('test finished')

    elif command == 'left':
        for i in range(iteration):
            print('turning left...')
            my_clawrobot.left()

        return ('Turning Left {} times'.format(iteration))

    elif command == 'right':
        for i in range(iteration):
            print('turning right...')
            my_clawrobot.right()

        return ('Turning Right {} times'.format(iteration))

    elif command == 'forward' or command == 'go':
        for i in range(iteration):
            print('moving forwards...')
            my_clawrobot.forward()

        return ('Moved Forward {} times'.format(iteration))

    elif command == 'backward' or command == 'reverse':
        for i in range(iteration):
            print('moving backwards...')
            my_clawrobot.reverse()

        return ('Moved Backward {} times'.format(iteration))

    elif command == 'commands':
        temp = 'Implemented Commands: '
        for command in commands:
            temp += command + ', '

        return temp

    else:
        print('ERROR: command not recognized: {}'.format(command))
        return 'Command not found!'

def listenToClient(client, address, my_clawrobot):
    size=1024
    while True:
        try:
            data = client.recv(size).decode()
            if data:
                # Read command from client
                print("from connected user: " + str(data))
                response = command_processor(data, my_clawrobot)

                # data = str(data).upper()
                client.send(response.encode())
            else:
                raise error('Client disconnected')
        except:
            client.close()
            return False

#def Main(host, port, config_file):
def Main(host, port):
    #my_clawrobot = initialize_clawrobot(config_file)
    my_clawrobot = initialize_clawrobot()

    mySocket = socket.socket()
    mySocket.bind((host,port))
     
    mySocket.listen(5)
    while True:
        client, address = mySocket.accept()
        client.settimeout(300)
        print ("Connection from: " + str(address))
        listenToClient(client, address, my_clawrobot)
     
if __name__ == '__main__':
    args = get_args()

    print('Host: {}'.format(args.host))
    print('Port: {}'.format(args.port))
    #print('Config File: {}'.format(args.config_file))

    #Main(args.host, args.port, args.config_file)
    Main(args.host, args.port)
