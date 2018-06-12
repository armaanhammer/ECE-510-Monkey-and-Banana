import argparse
import socket
import time
#import yaml

from ClawRobot import ClawRobot
 
def get_args():
    parser = argparse.ArgumentParser(description='clawrobot server.')

    parser.add_argument(
            '--host',
            default='192.168.0.100',
            help='host ip of the clawrobot')

    parser.add_argument(
            '--port',
            default=5001,
            type=int,
            help='port used to communicate to the clawrobot')

    return parser.parse_args()

#def initialize_clawrobot(config_file):
def initialize_clawrobot():
    my_clawrobot = ClawRobot(motors1_port='JC', motors2_port='JB', servos_port='JAB')
    my_clawrobot.stop()
    
    return my_clawrobot


def command_processor(data, my_clawrobot):
    delay = 0.1
    power = 50

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
        'stop',
    ]
    
    if command == 'open':
        print('Opening claw...')
        my_clawrobot.open_claw()
        return ('Opened claw')

    elif command == 'close':
        print('Closing claw...')
        my_clawrobot.close_claw()
        return ('Closed claw')

    elif command == '' or command == 'stop':
        print('Stopping')
        my_clawrobot.stop()
        return ('Stopped')

    elif command == 'test':
        print('test')
        return('test finished')

    elif command == 'left':
        for i in range(iteration):
            print('turning left...')
            my_clawrobot.left(delay=delay, power=power)

        return ('Turning Left {} times'.format(iteration))

    elif command == 'right':
        for i in range(iteration):
            print('turning right...')
            my_clawrobot.right(delay=delay, power=power)

        return ('Turning Right {} times'.format(iteration))

    elif command == 'forward' or command == 'go':
        for i in range(iteration):
            print('moving forwards...')
            my_clawrobot.forward(delay=delay, power=power)

        return ('Moved Forward {} times'.format(iteration))

    elif command == 'backward' or command == 'reverse':
        for i in range(iteration):
            print('moving backwards...')
            my_clawrobot.reverse(delay=delay, power=power)

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

    try:
        while True:
            client, address = mySocket.accept()
            client.settimeout(300)
            print ("Connection from: " + str(address))
            listenToClient(client, address, my_clawrobot)

    except KeyboardInterrupt as e:
        print('\nyou cancelled the operation.')
    finally:
        mySocket.close()
     
if __name__ == '__main__':
    args = get_args()

    print('Host: {}'.format(args.host))
    print('Port: {}'.format(args.port))
    
    Main(args.host, args.port)
