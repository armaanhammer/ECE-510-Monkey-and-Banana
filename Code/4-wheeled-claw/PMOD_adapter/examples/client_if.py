import argparse
import socket

# import object detection code
#import object_detection as od

def get_args():
    parser = argparse.ArgumentParser(description='claw client.')

    parser.add_argument(
            '--host',
            default='192.168.0.104',
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

#    parser.add_argument(
#            '-v',
#            '--vision',
#            action="store_true",
#            help='use OpenCV vision to move the claw bot')

    return parser.parse_args()

#def Main(host, port, script, vision=0):
def Main(host, port, script):
        mySocket = socket.socket()
        mySocket.connect((host,port))

#        if vision:
#            od.Main(mySocket=mySocket)
#            print('No Vision')

#        elif script:
        if script:
            with open(script) as f:
                for line in f:
                    mySocket.send(line.strip().encode())
                    data = mySocket.recv(1024).decode()

                    print('Recieved from server: ' + data)

        else:
            message = raw_input("cmd: ")

            while message != 'q':
                if message:
                    mySocket.send(message.encode())
                    data = mySocket.recv(1024).decode()

                    print ('Received from server: ' + data)

                message = raw_input("cmd: ")

        mySocket.close()

if __name__ == '__main__':
    args = get_args()

    print('Host: {}'.format(args.host))
    print('Port: {}'.format(args.port))
    print('Script: {}'.format(args.script))
#    print('Vision: {}'.format(args.vision))

#    Main(args.host, args.port, args.script, args.vision)
    Main(args.host, args.port, args.script)
