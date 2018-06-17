import argparse
from copy import deepcopy
import cv2
import cv2.aruco as aruco
import math
import numpy as np
from pprint import pprint
import socket
import time
import yaml
from pyswip import Prolog

# Prolog instance and input rules file
prolog = Prolog()
prolog.consult('prolog_planner1.pl')

# Aruco marker IDs for various scene objects
CAN_ID = 880

CLAW_ROBOT_ID = 481

TOP_RIGHT_RAMP_ID = 818
TOP_LEFT_RAMP_ID = 58
BOTTOM_RIGHT_RAMP_ID = 209
BOTTOM_LEFT_RAMP_ID = 839

TOP_RIGHT_SCENE_ID = 205
TOP_LEFT_SCENE_ID = 800
BOTTOM_RIGHT_SCENE_ID = 450
BOTTOM_LEFT_SCENE_ID = 630

# Scene Objects dictionary
scene_objects = {
    'can': {
        'name': 'CAN',
        'id': CAN_ID,
    },
    'claw': {
        'name': 'CLAW',
        'id': CLAW_ROBOT_ID,
    },
    'ramp': {
        'name': 'RAMP',
        'markers': [
            {
                'name': 'top_right',
                'id': TOP_RIGHT_RAMP_ID,
            },
            {
                'name': 'top_left',
                'id': TOP_LEFT_RAMP_ID,
            },
            {
                'name': 'bottom_right',
                'id': BOTTOM_RIGHT_RAMP_ID, 
            },
            {
                'name': 'bottom_left',
                'id': BOTTOM_LEFT_RAMP_ID,
            },
        ]
    },
    'scene': {
        'name': 'SCENE',
        'markers': [
            {
                'name': 'top_right',
                'id': TOP_RIGHT_SCENE_ID,
            },
            {
                'name': 'top_left',
                'id': TOP_LEFT_SCENE_ID,
            },
            {
                'name': 'bottom_right',
                'id': BOTTOM_RIGHT_SCENE_ID, 
            },
            {
                'name': 'bottom_left',
                'id': BOTTOM_LEFT_SCENE_ID,
            },
        ]
    }

}


# Command Line Arguements Parser
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
            '-c',
            '--calibration_file',
            default='camera_calibration_results.yml',
            help='OpenCV Calibration File')


    return parser.parse_args()


# Read the camera calibration data
def read_calibration_data(file):
    ret_val = []
    with open(file, 'r') as yaml_file:
        d = yaml.load(yaml_file)

        ret_val.append(d['retval'])
        ret_val.append(d['cameraMatrix'])
        ret_val.append(d['distCoeffs'])
        ret_val.append(d['rvecs'])
        ret_val.append(d['tvecs'])

    return ret_val


def get_distance(pt1, pt2):
    # X-direction is positive (increase when going from left to right) for both image and cartesian coordinates
    x = pt2[0] - pt1[0]

    # Y-direction is negative (increases going down the frame) for the image coordinates
    # and is positive (increases going up the frame) for the cartesian coordinates
    y = pt1[1] - pt2[1]
    distance = math.sqrt(x**2 + y**2)
    return distance


def get_angle(pt1, pt2):
    # X-direction is positive (increase when going from left to right) for both image and cartesian coordinates
    x = pt2[0] - pt1[0]

    # Y-direction is negative (increases going down the frame) for the image coordinates
    # and is positive (increases going up the frame) for the cartesian coordinates
    y = pt1[1] - pt2[1]

    abs_x = np.absolute(x)
    abs_y = np.absolute(y)
    tmp_angle = np.arctan(abs_y/abs_x)

    if x >= 0 and y >= 0:
        angle = ((1/2)*np.pi) - tmp_angle                    
    elif x >=0 and y < 0:
        angle = ((1/2)*np.pi) + tmp_angle
    elif x < 0 and y < 0:
        angle = ((3/2)*np.pi) - tmp_angle
    elif x < 0 and y >= 0:
        angle = ((3/2)*np.pi) + tmp_angle
    else:
        print("illegal angle!!!")
        print("x: {}".format(x))
        print("y: {}".format(y))
        print("angle: {}".format(tmp_angle))
        angle = np.NaN

    angle = angle * (180/np.pi)

    return angle


def draw_vectors(frame, centers, centers_2, ends):
    radius_inner = 3
    radius_outer = 5
    thickness = 2
    line = 8
    green = (0,0,255)
    red = (0,255,0)
    blue = (255,0,0)
    for center, center_2, end in zip(centers, centers_2, ends):
        # Draw the center as calculated by the find_center function
        center_pxs = tuple([int(x) for x in center])
        cv2.circle(frame, center_pxs, radius_outer, red, -1)

        # Draw the center as returned by the projectPoints function
        center_2_pxs = tuple([int(x) for x in center_2])
        cv2.circle(frame, center_2_pxs, radius_inner, green, -1)

        # Draw the line from the center to the end of the directional vector
        # That was generated from the projectPoints function
        end_pxs = tuple([int(x) for x in end])
        cv2.line(frame, center_pxs, end_pxs, blue, thickness=thickness, lineType=line, shift=0)


def draw_centers(frame, centers):
    radius = 5
    color = (0,0,255) # Red
    for center in centers:
        center_pxs = tuple([int(x) for x in center])
        cv2.circle(frame, center_pxs, radius, color, -1)



def find_center(cnrs):
    x = cnrs[0][0][0] + cnrs[0][1][0] + cnrs[0][2][0] + cnrs[0][3][0]
    x = x/4
    y = cnrs[0][0][1] + cnrs[0][1][1] + cnrs[0][2][1] + cnrs[0][3][1]
    y = y/4
    return([x,y])
  

def find_all_centers(cnrs_list):
    centers = []
    for cnrs in cnrs_list:
        centers.append(find_center(cnrs))

    return centers


def find_front(crns):
  pass


def print_object_info(obj):
    # if the object has a markers list, print each marker in the list
    if 'markers' in obj.keys():
        for marker in obj['markers']:
            print_object_info(marker)
    
    # Print ID
    if 'id' in obj.keys():
        print('{} ID: {}'.format(obj['name'], obj['id']))

    # Print Position
    if 'position' in obj.keys():
        print('{0} position: ({1:.0f}, {2:.0f})'.format(obj['name'], 
                                             obj['position'][0], 
                                             obj['position'][1]))

    # Print Angle
    if 'angle' in obj.keys():
        print('{0} angle: {1:.1f}'.format(obj['name'], obj['angle']))
    
    print()


def update_obj(obj, center, front):
    obj['position'] = tuple([int(x) for x in center])
    obj['front'] = tuple([int(x) for x in front])
    obj['angle'] = get_angle(center, front)

    return obj

def get_claw_to_can_distance(scene_objects):
    distance = np.NaN
    if 'position' in scene_objects['claw']:
        claw_pt = scene_objects['claw']['position']
    else:
        claw_pt = None

    if 'position' in scene_objects['can']:
        can_pt = scene_objects['can']['position']
    else:
        can_pt = None

    if claw_pt is not None and can_pt is not None:
        distance = get_distance(claw_pt, can_pt)

    print('Claw to Can distance: {0:1f}'.format(distance))

    return distance


def get_claw_to_can_angle(frame, scene_objects):
    # calculate angle between the can and the claw
    black = (0, 0, 0)
    if 'position' in scene_objects['claw']:
        claw_pt = scene_objects['claw']['position']
    else:
        claw_pt = None
    
    if 'angle' in scene_objects['claw']:
        claw_ang = scene_objects['claw']['angle']
    else:
        claw_ang = np.NaN
    
    if 'position' in scene_objects['can']:
        can_pt = scene_objects['can']['position']
    else:
        can_pt = None

    if claw_pt is not None and can_pt is not None:
        cv2.line(frame, claw_pt, can_pt, black, thickness=2, lineType=8, shift=0)

    if claw_pt is not None and can_pt is not None:
        claw_to_can_vector_angle = get_angle(claw_pt, can_pt)
    else:
        claw_to_can_vector_angle = np.NaN

    if not np.isnan(claw_to_can_vector_angle):
        claw_to_can_angle = claw_to_can_vector_angle - claw_ang
        if claw_to_can_angle < 0:
            claw_to_can_angle = claw_to_can_angle + 360
    else:
        claw_to_can_angle = np.NaN

    print('Claw to Can angle: {0:1f}'.format(claw_to_can_angle))

    return claw_to_can_angle


def send_command(socket, message):
    socket.send(message.encode())
    data = socket.recv(1024).decode()


def update_claw(claw_to_can_distance, claw_to_can_angle, mySocket, move_robot=True):
    angle_buffer = 10
    max_distance = 50

    max_angle = int(360 - (angle_buffer/2))
    min_angle = int((angle_buffer/2))

    threshold_angle = 180

    claw_to_can_angle = int(claw_to_can_angle)
    claw_to_can_distance = int(claw_to_can_distance)

    move_forward_and_open_query = "move_forward_and_open({0:}, {1:}, {2:}, {3:}, {4:})".format(
        claw_to_can_angle, 
        claw_to_can_distance,
        max_angle,
        min_angle,
        max_distance
    )
    print(move_forward_and_open_query)
    move_forward_and_open = bool(list(prolog.query(move_forward_and_open_query)))

    stop_and_close_query = "stop_and_close({0:}, {1:}, {2:}, {3:}, {4:})".format(
        claw_to_can_angle, 
        claw_to_can_distance,
        max_angle,
        min_angle,
        max_distance
    )
    print(stop_and_close_query)
    stop_and_close = bool(list(prolog.query(stop_and_close_query)))

    can_move_left_query = "can_move_left({0:},{1:})".format(claw_to_can_angle, threshold_angle)
    print(can_move_left_query)
    can_move_left = bool(list(prolog.query(can_move_left_query)))

    print()
    
    if(move_forward_and_open):
        print('open')
        print('forward')
        if move_robot:
            send_command(mySocket, 'open')
            send_command(mySocket, 'forward')
    elif(stop_and_close):
        print('stop')
        print('close')
        if move_robot:
            send_command(mySocket, 'stop')
            send_command(mySocket, 'close')
    elif(can_move_left):
        print('turn left')
        if move_robot:
            send_command(mySocket, 'left')
    else:
        print('turn right')
        if move_robot:
            send_command(mySocket, 'right')


def setup_video_capture_device(device_id=1):
    # setup camera capture
    cap = cv2.VideoCapture(1)

    # Adjust camera settings (resolution, autofocus, etc.)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 720)
    # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    # This is used to pop up the camera settings for scenarios where the settings cannot be set using OpenCV commands
    # cap.set(cv2.CAP_PROP_SETTINGS, 1)

    # is it set correctly?
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)

    # wtf autofocus?
    autofocus = cap.set(cv2.CAP_PROP_AUTOFOCUS, 0) # turn off autofocus
    print(autofocus)
    print(cap.get(cv2.CAP_PROP_AUTOFOCUS))

    return cap


def main_vision(host, port, calibration_file):
    length = 0.04 # length of marker side
    count = 0
    max_count = 10
    show_frame = True
    move_robot = False
    use_video = True
    save_frame = True 

    if move_robot:
        # get socket for claw robot server connection
        print('Opening socket connection to Claw Robot')
        mySocket = socket.socket()
        mySocket.connect((host,port))
    else:
        mySocket = None

    # Get calibration results from input file   
    print('Reading camera calibration data from file')     
    (retval, cameraMatrix, distCoeffs, rvecs_orig, tvecs_orig) = read_calibration_data(calibration_file)

    # Use default dictionary for aruco marker definitions
    dictionary = aruco.getPredefinedDictionary(aruco.DICT_ARUCO_ORIGINAL)

    print('Setting up video capture device')
    cap = setup_video_capture_device(device_id=1)

    axisPoints = np.array([[0,0,0],[length,0,0],[0,length,0],[0,0,length]])

    cv2.namedWindow('frame', cv2.WINDOW_NORMAL)

    try:
        while cap.isOpened():
            flags, frame = cap.read()
            frame_to_save = deepcopy(frame)

            if not use_video:
                frame = cv2.imread('good_sample.png')

            corners, ids, rejectedImgPoints = aruco.detectMarkers(frame, dictionary)

            if len(corners)>0:
                # print('Detected markers')
                
                centers_calc = find_all_centers(corners)
                # draw_centers(frame, centers_calc)

                # aruco.drawDetectedMarkers(frame, corners, ids)
                
                rvecs, tvecs, obj_points = aruco.estimatePoseSingleMarkers(corners, length, cameraMatrix, distCoeffs)
                
                centers = []
                fronts = []
                for rvec, tvec in zip(rvecs, tvecs):
                    # aruco.drawAxis(frame, cameraMatrix, distCoeffs, rvec, tvec, length)
                    
                    # Populate object locations
                    imgPoints, ret = cv2.projectPoints(axisPoints, rvec, tvec, cameraMatrix, distCoeffs)

                    centers.append([imgPoints[0][0][0],imgPoints[0][0][1]])
                    fronts.append([imgPoints[1][0][0],imgPoints[1][0][1]])
                
                draw_vectors(frame, centers_calc, centers, fronts)

                for id, center, front in zip(ids, centers, fronts):
                    for (key, obj) in scene_objects.items():
                        if 'id' in obj.keys() and id == obj['id']:
                            obj = update_obj(obj, center, front)
                        elif 'markers' in obj.keys():
                            for marker in obj['markers']:
                                if id == marker['id']:
                                    marker = update_obj(marker, center, front)

            # print all objects ID/POSITION/ANGLE
            for (key, obj) in scene_objects.items():
                print_object_info(obj)

            print(10*'-')
            claw_to_can_angle = get_claw_to_can_angle(frame, scene_objects)
            print(10*'-')
            claw_to_can_distance = get_claw_to_can_distance(scene_objects)
            print(10*'-')
            print()

            if count > max_count:
                count = 0
                
                if not np.isnan(claw_to_can_angle):
                    update_claw(claw_to_can_distance, claw_to_can_angle, mySocket, move_robot=move_robot)

                time.sleep(1)
            else:
                count += 1

            if show_frame:
                frame2 = cv2.resize(frame, (800, 600)) 
                cv2.imshow('frame', frame2)

                if save_frame and len(ids) == 8:
                    cv2.imwrite('frame_snapshot.png', frame_to_save)
                
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        print('You cancelled the operation.')
    finally:
        print()
        print('Releasing Capture device')
        
        cap.release()

        print('Closing OpenCV Windows')
        cv2.destroyAllWindows()

        if move_robot:
            # clean up claw robot server connection
            print('Releasing Claw Robot Socket')
            mySocket.close()
        print()

if __name__ == '__main__':
    args = get_args()

    print('Host: {}'.format(args.host))
    print('Port: {}'.format(args.port))
    print('Calibration File: {}'.format(args.calibration_file))

    main_vision(args.host, args.port, args.calibration_file)
