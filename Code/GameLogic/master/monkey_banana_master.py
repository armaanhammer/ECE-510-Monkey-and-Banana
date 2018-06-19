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
prolog.consult('monkey_banana_rules.pl')

# Aruco marker IDs for various scene objects
CAN_ID = 880

CLAW_ROBOT_FRONT_ID = 481
CLAW_ROBOT_CENTER_ID = 400

TOP_RIGHT_RAMP_ID = 818
TOP_LEFT_RAMP_ID = 58
BOTTOM_RIGHT_RAMP_ID = 209
BOTTOM_LEFT_RAMP_ID = 839

TOP_RIGHT_SCENE_ID = 420
TOP_LEFT_SCENE_ID = 800
BOTTOM_RIGHT_SCENE_ID = 450
BOTTOM_LEFT_SCENE_ID = 630

# Scene Objects dictionary
scene_objects = {
    'can': {
        'name': 'CAN',
        'id': CAN_ID,
    },
    'claw_center': {
        'name': 'CLAW_CENTER',
        'id': CLAW_ROBOT_CENTER_ID,
    },
    'claw_front': {
        'name': 'CLAW_FRONT',
        'id': CLAW_ROBOT_FRONT_ID,
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
    if pt1 is not None and pt2 is not None:
        # X-direction is positive (increase when going from left to right) for both image and cartesian coordinates
        x = pt2[0] - pt1[0]

        # Y-direction is negative (increases going down the frame) for the image coordinates
        # and is positive (increases going up the frame) for the cartesian coordinates
        y = pt1[1] - pt2[1]
        distance = math.sqrt(x**2 + y**2)
    else:
        distance = np.NaN

    return distance


def get_angle(pt1, pt2):
    if pt1 is not None and pt2 is not None:
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
    else:
        angle = np.NaN

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
        if center_2_pxs[0] > 2000 or \
                center_2_pxs[1] > 2000 or \
                center_2_pxs[0] < 0 or \
                center_2_pxs[1] < 0:
            pass
        else:
            cv2.circle(frame, center_2_pxs, radius_inner, green, -1)

        # Draw the line from the center to the end of the directional vector
        # That was generated from the projectPoints function
        end_pxs = tuple([int(x) for x in end])
        if end_pxs[0] > 2000 or \
                end_pxs[1] > 2000 or \
                end_pxs[0] < 0 or \
                end_pxs[1] < 0:
            pass
        else:
            cv2.line(frame, center_pxs, end_pxs, blue, thickness=thickness, lineType=line, shift=0)


def draw_centers(frame, centers):
    radius = 5
    color = (0,0,255) # Red
    for center in centers:
        center_pxs = tuple([int(x) for x in center])
        cv2.circle(frame, center_pxs, radius, color, -1)


def find_center(cnrs):
    x = [x[0] for x in cnrs]
    avg_x = np.average(x)

    y = [x[1] for x in cnrs]
    avg_y = np.average(y)
    
    return tuple([int(avg_x), int(avg_y)])


def find_all_centers(cnrs_list):
    centers = []
    for cnrs in cnrs_list:
        centers.append(find_center(cnrs[0]))

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


def get_claw_to_goal_distance(claw_pt, goal_pt, verbose=True):
    distance = np.NaN

    if claw_pt is not None and goal_pt is not None:
        distance = get_distance(claw_pt, goal_pt)

    if verbose:
        print('Claw to Goal distance: {0:1f}'.format(distance))

    return distance


def get_claw_to_goal_angle(claw_pt, claw_angle, goal_pt, verbose=True):
    claw_to_goal_vector_angle = get_angle(claw_pt, goal_pt)

    if not np.isnan(claw_to_goal_vector_angle):
        claw_to_goal_angle = claw_to_goal_vector_angle - claw_angle
        if claw_to_goal_angle < 0:
            claw_to_goal_angle = claw_to_goal_angle + 360
    else:
        claw_to_goal_angle = np.NaN

    if verbose:
        print('Claw to Goal angle: {0:1f}'.format(claw_to_goal_angle))

    return claw_to_goal_angle


def send_command(socket, message):
    socket.send(message.encode())
    data = socket.recv(1024).decode()


def update_claw(claw_to_goal_distance, claw_to_goal_angle, mySocket, goal, move_robot=True, verbose=False, start=True, win=False):
    if start:
        if move_robot:
            send_command(mySocket, 'open')
        return 'open'

    if win:
        if move_robot:
            send_command(mySocket, 'forward')
            send_command(mySocket, 'close')
            send_command(mySocket, 'stop')
        return 'stop'

    angle_buffer = 10

    if goal == 'can':
        max_distance = 70
    else:
        max_distance = 25

    max_angle = int(360 - (angle_buffer/2))
    min_angle = int((angle_buffer/2))

    threshold_angle = 180

    if np.isnan(claw_to_goal_angle):
        return 'error'
    
    if np.isnan(claw_to_goal_distance):
        return 'error'

    claw_to_goal_angle = int(claw_to_goal_angle)
    claw_to_goal_distance = int(claw_to_goal_distance)

    forward_query = "forward({0:}, {1:}, {2:}, {3:}, {4:})".format(
        claw_to_goal_angle, 
        claw_to_goal_distance,
        max_angle,
        min_angle,
        max_distance
    )
    if verbose:
        print(forward_query)
    forward = bool(list(prolog.query(forward_query)))

    stop_query = "stop({0:}, {1:})".format(
        claw_to_goal_distance,
        max_distance
    )
    if verbose:
        print(stop_query)
    stop = bool(list(prolog.query(stop_query)))

    left_query = "left({0:},{1:})".format(claw_to_goal_angle, threshold_angle)
    if verbose:
        print(left_query)
    left = bool(list(prolog.query(left_query)))

    if(forward): command = 'forward'
    elif(stop): command = 'stop'
    elif(left): command = 'left'
    else: command = 'right'
    
    # Print the command if verbose
    if verbose:
        print('Command: {}'.format(command))

    # move the robot if flag is set to true
    if move_robot:
        delay = "0.1"

        if command == 'left' or command == 'right':
            if claw_to_goal_angle > 90:
                delay = "0.2"
            elif claw_to_goal_angle > 45:
                delay = "0.15"
            else:
                delay = "0.1"

        if command == 'forward':
            if goal == 'can':
                if claw_to_goal_distance > 200:
                    delay = "0.3"
                elif claw_to_goal_distance > 150:
                    delay = "0.25"
                else:
                    delay = "0.2"
            else:
                if claw_to_goal_distance > 200:
                    delay = "0.2"
                elif claw_to_goal_distance > 150:
                    delay = "0.15"
                else:
                    delay = "0.1"

        power = "50"

        if command == 'stop':
            delay = "0.0"
            power = "0"            

        full_command = command + " " + delay + " " + power
        send_command(mySocket, full_command)

    return command


def setup_video_capture_device(device_id=0):
    # setup camera capture
    cap = cv2.VideoCapture(device_id)

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


def draw_line(frame, pt1, pt2, color):
    thickness = 2
    line = 8
    green = (0,0,255)
    red = (0,255,0)
    blue = (255,0,0)
    black = (0,0,0)

    pt1_pxs = tuple([int(x) for x in pt1])
    pt2_pxs = tuple([int(x) for x in pt2])

    if pt1_pxs[0] > 2000 or \
            pt1_pxs[1] > 2000 or \
            pt1_pxs[0] < 0 or \
            pt1_pxs[1] < 0 or \
            pt2_pxs[0] > 2000 or \
            pt2_pxs[1] > 2000 or \
            pt2_pxs[0] < 0 or \
            pt2_pxs[1] < 0:
        pass
    else:
        cv2.line(frame, pt1_pxs, pt2_pxs, color, thickness=thickness, lineType=line, shift=0)


def draw_box(frame, corners, color):
    draw_line(frame, corners[0], corners[1], color)
    draw_line(frame, corners[1], corners[3], color)
    draw_line(frame, corners[2], corners[3], color)
    draw_line(frame, corners[2], corners[0], color)


def find_region_center(region):
    corners = [region['top_left'], region['top_right'], region['bottom_left'], region['bottom_right']]
    region['center'] = find_center(corners)
    return region


def get_position(corners, name):
    position = [x['position'] for x in corners if x['name'] == name and 'position' in x.keys()]
    if len(position) > 0:
        return position[0]
    else:
        return None

def get_top_left_region(scene_corners, ramp_corners, verbose=False):
    scene_top_left = get_position(scene_corners, 'top_left')
    if scene_top_left is None: return None

    ramp_top_left = get_position(ramp_corners, 'top_left')
    if ramp_top_left is None: return None

    region = {
        'name': 'top_left',
        'top_left': scene_top_left,
        'bottom_right': ramp_top_left,
        'top_right': (ramp_top_left[0], scene_top_left[1]),
        'bottom_left': (scene_top_left[0], ramp_top_left[1]),
    }

    region = find_region_center(region)

    if verbose:
        pprint(region)

    return region


def get_bottom_left_region(scene_corners, ramp_corners, verbose=False):
    scene_bottom_left = get_position(scene_corners, 'bottom_left')
    if scene_bottom_left is None: return None

    ramp_bottom_left = get_position(ramp_corners, 'bottom_left')
    if ramp_bottom_left is None: return None 

    region = {
        'name': 'bottom_left',
        'bottom_left': scene_bottom_left,
        'top_right': ramp_bottom_left,
        'top_left': (scene_bottom_left[0], ramp_bottom_left[1]),
        'bottom_right': (ramp_bottom_left[0], scene_bottom_left[1]),
    }

    region = find_region_center(region)

    if verbose:
        pprint(region)

    return region


def get_bottom_right_region(scene_corners, ramp_corners, verbose=False):
    scene_bottom_right = get_position(scene_corners, 'bottom_right')
    if scene_bottom_right is None: return None 

    ramp_bottom_right = get_position(ramp_corners, 'bottom_right')
    if ramp_bottom_right is None: return None 
    
    region = {
        'name': 'bottom_right',
        'bottom_right': scene_bottom_right,
        'top_left': ramp_bottom_right,
        'top_right': (scene_bottom_right[0], ramp_bottom_right[1]),
        'bottom_left': (ramp_bottom_right[0], scene_bottom_right[1]),
    }

    region = find_region_center(region)

    if verbose:
        pprint(region)

    return region


def get_top_right_region(scene_corners, ramp_corners, verbose=False):
    scene_top_right = get_position(scene_corners, 'top_right')
    if scene_top_right is None: return None

    ramp_top_right = get_position(ramp_corners, 'top_right')
    if ramp_top_right is None: return None 

    region = {
        'name': 'top_right',
        'top_right': scene_top_right,
        'bottom_left': ramp_top_right,
        'top_left': (ramp_top_right[0], scene_top_right[1]),
        'bottom_right': (scene_top_right[0], ramp_top_right[1]),
    }

    region = find_region_center(region)

    if verbose:
        pprint(region)

    return region



def get_top_center_region(scene_corners, ramp_corners, verbose=False):
    scene_top_right = get_position(scene_corners, 'top_right')
    if scene_top_right is None: return None
    
    scene_top_left = get_position(scene_corners, 'top_left')
    if scene_top_left is None: return None

    top_y_value = np.average([scene_top_right[1], scene_top_left[1]])

    ramp_top_right = get_position(ramp_corners, 'top_right')
    if ramp_top_right is None: return None

    ramp_top_left = get_position(ramp_corners, 'top_left')
    if ramp_top_left is None: return None 

    region = {
        'name': 'top_center',
        'top_right': (ramp_top_right[0], top_y_value),
        'bottom_left': ramp_top_left,
        'top_left': (ramp_top_left[0], top_y_value),
        'bottom_right': ramp_top_right,
    }

    region = find_region_center(region)

    if verbose:
        pprint(region)

    return region


def get_bottom_center_region(scene_corners, ramp_corners, verbose=False):
    scene_bottom_right = get_position(scene_corners, 'bottom_right')
    if scene_bottom_right is None: return None

    scene_bottom_left = get_position(scene_corners, 'bottom_left')
    if scene_bottom_left is None: return None

    bottom_y_value = np.average([scene_bottom_right[1], scene_bottom_left[1]])

    ramp_bottom_right = get_position(ramp_corners, 'bottom_right')
    if ramp_bottom_right is None: return None

    ramp_bottom_left = get_position(ramp_corners, 'bottom_left')
    if ramp_bottom_left is None: return None

    region = {
        'name': 'bottom_center',
        'top_right': ramp_bottom_right,
        'bottom_left': (ramp_bottom_left[0], bottom_y_value),
        'top_left': ramp_bottom_left,
        'bottom_right': (ramp_bottom_right[0], bottom_y_value),
    }

    region = find_region_center(region)

    if verbose:
        pprint(region)

    return region


def get_center_left_region(scene_corners, ramp_corners, verbose=False):
    scene_top_left = get_position(scene_corners, 'top_left')
    if scene_top_left is None: return None

    scene_bottom_left = get_position(scene_corners, 'bottom_left')
    if scene_bottom_left is None: return None

    left_x_value = np.average([scene_top_left[0], scene_bottom_left[0]])

    ramp_top_left = get_position(ramp_corners, 'top_left')
    if ramp_top_left is None: return None

    ramp_bottom_left = get_position(ramp_corners, 'bottom_left')
    if ramp_bottom_left is None: return None

    region = {
        'name': 'center_left',
        'top_right': ramp_top_left,
        'bottom_left': (left_x_value, ramp_bottom_left[1]),
        'top_left': (left_x_value, ramp_top_left[1]),
        'bottom_right': ramp_bottom_left,
    }

    region = find_region_center(region)

    if verbose:
        pprint(region)

    return region


def get_center_right_region(scene_corners, ramp_corners, verbose=False):
    scene_top_right = get_position(scene_corners, 'top_right')
    if scene_top_right is None: return None

    scene_bottom_right = get_position(scene_corners, 'bottom_right')
    if scene_bottom_right is None: return None

    right_x_value = np.average([scene_top_right[0], scene_bottom_right[0]])

    ramp_top_right = get_position(ramp_corners, 'top_right')
    if ramp_top_right is None: return None

    ramp_bottom_right = get_position(ramp_corners, 'bottom_right')
    if ramp_bottom_right is None: return None

    region = {
        'name': 'center_right',
        'top_right': (right_x_value, ramp_top_right[1]),
        'bottom_left': ramp_bottom_right,
        'top_left': ramp_top_right,
        'bottom_right': (right_x_value, ramp_bottom_right[1]),
    }

    region = find_region_center(region)

    if verbose:
        pprint(region)

    return region


def get_center_region(scene_corners, ramp_corners, verbose=False):
    ramp_top_right = get_position(ramp_corners, 'top_right')
    if ramp_top_right is None: return None

    ramp_bottom_right = get_position(ramp_corners, 'bottom_right')
    if ramp_bottom_right is None: return None

    ramp_top_left = get_position(ramp_corners, 'top_left')
    if ramp_top_left is None: return None

    ramp_bottom_left = get_position(ramp_corners, 'bottom_left')
    if ramp_bottom_left is None: return None

    region = {
        'name': 'center',
        'top_right': ramp_top_right,
        'bottom_left': ramp_bottom_left,
        'top_left': ramp_top_left,
        'bottom_right': ramp_bottom_right,
    }

    region = find_region_center(region)

    if verbose:
        pprint(region)

    return region


def draw_region(frame, region, color):
    if region:
        region_corners = [region['top_left'], 
                          region['top_right'],
                          region['bottom_left'], 
                          region['bottom_right']]
        draw_box(frame, region_corners, color)
        draw_centers(frame, [region['center']])


def get_regions(scene_objects, regions):
    scene_corners = scene_objects['scene']['markers']
    ramp_corners = scene_objects['ramp']['markers']

    top_left_region = get_top_left_region(scene_corners, ramp_corners)
    bottom_left_region = get_bottom_left_region(scene_corners, ramp_corners)
    bottom_right_region = get_bottom_right_region(scene_corners, ramp_corners)
    top_right_region = get_top_right_region(scene_corners, ramp_corners)
    top_center_region = get_top_center_region(scene_corners, ramp_corners)
    bottom_center_region = get_bottom_center_region(scene_corners, ramp_corners)
    center_left_region = get_center_left_region(scene_corners, ramp_corners)
    center_right_region = get_center_right_region(scene_corners, ramp_corners)
    center_region = get_center_region(scene_corners, ramp_corners)

    if top_left_region is not None:
        regions['top_left'] = top_left_region
    
    if bottom_left_region is not None:
        regions['bottom_left'] = bottom_left_region

    if top_right_region is not None:
        regions['top_right'] = top_right_region
    
    if bottom_right_region is not None:
        regions['bottom_right'] = bottom_right_region

    if top_center_region is not None:
        regions['top_center'] = top_center_region
    
    if bottom_right_region is not None:
        regions['bottom_center'] = bottom_center_region

    if center_left_region is not None:
        regions['center_left'] = center_left_region

    if center_right_region is not None:
        regions['center_right'] = center_right_region

    if center_region is not None:
        regions['center'] = center_region

    return regions


def draw_scene_regions(frame, regions):
    for key, value in regions.items():
        draw_region(frame, value, (0,0,0))


def update_scene_objects(scene_objects, ids, centers, fronts):
    for id, center, front in zip(ids, centers, fronts):
        for (key, obj) in scene_objects.items():
            if 'id' in obj.keys() and id == obj['id']:
                obj = update_obj(obj, center, front)
            elif 'markers' in obj.keys():
                for marker in obj['markers']:
                    if id == marker['id']:
                        marker = update_obj(marker, center, front)
    return scene_objects


def get_centers_and_fronts(rvecs, tvecs, axisPoints, cameraMatrix, distCoeffs):
    centers = []
    fronts = []
    for rvec, tvec in zip(rvecs, tvecs):
        # aruco.drawAxis(frame, cameraMatrix, distCoeffs, rvec, tvec, length)
        
        # Populate object locations
        imgPoints, ret = cv2.projectPoints(axisPoints, rvec, tvec, cameraMatrix, distCoeffs)

        centers.append([imgPoints[0][0][0],imgPoints[0][0][1]])
        fronts.append([imgPoints[1][0][0],imgPoints[1][0][1]])
    return (centers, fronts)


def get_goal_position(goal, scene_objects, regions):
    # Default to None
    position = None

    if goal == 'can':
         if 'position' in scene_objects['can']:
            position = scene_objects['can']['position']
    elif goal in regions.keys():
        position = regions[goal]['center']
    else:
        print("ERROR: Unknown goal: {}".format(goal))
        
    return position


def get_claw_position(scene_objects, front=False):
    position = None

    if front:
        name = 'claw_front'
    else:
        name = 'claw_center'

    if 'position' in scene_objects[name]:
        position = scene_objects[name]['position']

    return position


def get_claw_angle(scene_objects, front=True):
    angle = None

    if front:
        name = 'claw_front'
    else:
        name = 'claw_center'

    if 'angle' in scene_objects[name]:
        angle = scene_objects[name]['angle']

    return angle


def is_claw_in_region(claw_position, region):
    x = claw_position[0]
    y = claw_position[1]

    if region is not None:
        if x > region['top_left'][0] and \
            x < region['top_right'][0] and \
            y > region['top_left'][1] and \
            y < region['bottom_left'][1]:
            return True
        else:
            return False
    else:
        return False

def get_claw_region(claw_position, regions):
    for _, region in regions.items():
        result = is_claw_in_region(claw_position, region)
        if result:
            return region['name']

    return None


def get_current_goal(current_region, verbose=False):
    query = "target({0:}, X)".format(current_region)
    if verbose:
        print(query)

    result = list(prolog.query(query))

    if verbose:
        print(result)

    if len(result) > 0:
        return result[0]['X']
    else:
        return None


def main_vision(host, port, calibration_file):
    global scene_objects

    length = 0.04 # length of marker side
    count = 0
    max_count = 5

    # Flags used to assist in debug
    show_frame = True
    move_robot = True
    use_video = True
    save_frame = False

    # Instantiate local variables
    start = True
    win = False
    state = None
    regions = {}
    current_region = None
    goal = None

    # axisPoints allow for drawing axis vectors
    axisPoints = np.array([[0,0,0],[length,0,0],[0,length,0],[0,0,length]])

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
    cap = setup_video_capture_device(device_id=0)

    # use a named window in normal mode allowing resizing
    cv2.namedWindow('frame', cv2.WINDOW_NORMAL)

    try:
        while cap.isOpened():
            # Capture the video frame from the camera
            flags, frame = cap.read()

            # Copy the raw frame to save for later (only if you specify the save_frame flag)
            if save_frame:
                frame_to_save = deepcopy(frame)

            # Read a static test image if use_video is false
            if not use_video:
                frame = cv2.imread('good_sample.png')

            # Detect the ArUco markers
            corners, ids, rejectedImgPoints = aruco.detectMarkers(frame, dictionary)

            # if there are markers detected, process them
            if len(corners)>0:
                # print('Detected markers')
                
                centers_calc = find_all_centers(corners)

                rvecs, tvecs, obj_points = aruco.estimatePoseSingleMarkers(corners, length, cameraMatrix, distCoeffs)
                
                (centers, fronts) = get_centers_and_fronts(rvecs, tvecs, axisPoints, cameraMatrix, distCoeffs)

                draw_vectors(frame, centers_calc, centers, fronts)

                scene_objects = update_scene_objects(scene_objects, ids, centers, fronts)

            # Get Regions (these shouldn't change)
            regions = get_regions(scene_objects, regions)
            draw_scene_regions(frame, regions)

            # Get claw position and angle
            if goal == 'can':
                claw_position = get_claw_position(scene_objects, front=True)
            else:
                claw_position = get_claw_position(scene_objects, front=False)

            claw_angle = get_claw_angle(scene_objects)

            # Get the current region of the claw
            if claw_position is not None:
                current_region = get_claw_region(claw_position, regions)

            print('Current Region: {}'.format(current_region))
            print('Current State: {}'.format(state))

            # Get goal, only want to update based on "stop" state
            if (start or state == 'stop') and current_region is not None:
                print('updating goal')
                print('old goal: {}'.format(goal))
                goal = get_current_goal(current_region)
                print('new goal: {}'.format(goal))
            
            print('Current Goal: {}'.format(goal))
            
            # Get goal position
            goal_position = get_goal_position(goal, scene_objects, regions)

            if claw_position is not None and goal_position is not None:
                draw_line(frame, claw_position, goal_position, (255,0,255))

            # Get distance to the goal
            goal_distance = get_claw_to_goal_distance(claw_position, goal_position, verbose=False)

            # Get angle to the goal
            goal_angle = get_claw_to_goal_angle(claw_position, claw_angle, goal_position, verbose=False)

            if count > max_count:
                count = 0
                
                if goal_angle is not None and goal_distance is not None:
                    state = update_claw(goal_distance, goal_angle, mySocket, goal, move_robot=move_robot, start=start, win=win)

                    print(state)

                # Check if we won
                if goal == 'can' and state == 'stop': 
                    win = True
                    print('We win!!!')
                
                if start and current_region is not None: 
                    start = False

                time.sleep(1)
            else:
                count += 1

            if show_frame:
                frame2 = cv2.resize(frame, (800, 600)) 
                cv2.imshow('frame', frame2)

                if save_frame and len(ids) == 8:
                    cv2.imwrite('frame_snapshot.png', frame)
                
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
