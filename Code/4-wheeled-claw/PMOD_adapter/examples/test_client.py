import argparse
import socket
import time

def get_args():
    parser = argparse.ArgumentParser(description='claw client.')

    parser.add_argument(
            '--host',
            default='192.168.0.100',
            help='host ip of the claw')

    parser.add_argument(
            '--port',
            default=5001,
            type=int,
            help='port used to communicate to the claw')

    parser.add_argument(
            '-s',
            '--script',
            default=None,
            help='script file to run claw')

    return parser.parse_args()


def send_command(socket, message):
    socket.send(message.encode())
    data = socket.recv(1024).decode()


def Main(host, port):
    mySocket = socket.socket()
    mySocket.connect((host,port))

    for i in range(4):
        message = 'forward'   # remove "raw_" for python3

        send_command(mySocket, message)
        time.sleep(2)

    # mySocket.send(message.encode())
    # data = mySocket.recv(1024).decode()

    mySocket.close()


if __name__ == '__main__':
    args = get_args()

    print('Host: {}'.format(args.host))
    print('Port: {}'.format(args.port))

    Main(args.host, args.port)
