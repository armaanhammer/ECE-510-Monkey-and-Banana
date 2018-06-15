import numpy as np
import cv2
import cv2.aruco as aruco
from pprint import pprint
import time
import yaml

CAN_ID = 880
CLAW_ROBOT_ID = 481

scene_objects = {
    'can': {
        'name': 'CAN',
        'id': CAN_ID,
    },
    'claw': {
        'name': 'CLAW',
        'id': CLAW_ROBOT_ID,
    }
}


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


def get_angle(center, end):
    x = end[0] - center[0]
    # y = end[1] - center[1]
    # x = center[0] - end[0]
    y = center[1] - end[1]

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
        angle = np.isnan

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
    print(10*'-')
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
    
    print(10*'-')


def update_obj(obj, center, front):
    obj['position'] = tuple([int(x) for x in center])
    obj['front'] = tuple([int(x) for x in front])
    obj['angle'] = get_angle(center, front)

    return obj


def get_claw_to_can_angle(frame, scene_objects):
        # calculate angle between the can and the claw
        black = (0, 0, 0)
        claw_pt = scene_objects['claw']['position']
        claw_ang = scene_objects['claw']['angle']
        can_pt = scene_objects['can']['position']

        cv2.line(frame, claw_pt, can_pt, black, thickness=2, lineType=8, shift=0)

        claw_to_can_vector_angle = get_angle(claw_pt, can_pt)
        print('Claw to Can vector angle: {0:.1f}'.format(claw_to_can_vector_angle))
        print(10*'-')

        claw_to_can_angle = claw_to_can_vector_angle - claw_ang
        if claw_to_can_angle < 0:
            claw_to_can_angle = claw_to_can_angle + 360

        print('Claw Angle: {0:1f}'.format(scene_objects['claw']['angle']))
        print('Claw to Can angle: {0:1f}'.format(claw_to_can_angle))
        print(10*'-')
        print()

        return claw_to_can_angle


def main():
    length = 0.04 # length of marker side
    count = 0
    max_count = 15

    # Get calibration results from input file            
    (retval, cameraMatrix, distCoeffs, rvecs_orig, tvecs_orig) = read_calibration_data('camera_calibration_results.yml')

    # Use default dictionary for aruco marker definitions
    dictionary = aruco.getPredefinedDictionary(aruco.DICT_ARUCO_ORIGINAL)

    # setup camera capture
    cap = cv2.VideoCapture(1)

    # Adjust camera settings (resolution, autofocus, etc.)
    # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 720)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    # This is used to pop up the camera settings for scenarios where the settings cannot be set using OpenCV commands
    # cap.set(cv2.CAP_PROP_SETTINGS, 1)

    # is it set correctly?
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)

    # wtf autofocus?
    autofocus = cap.set(cv2.CAP_PROP_AUTOFOCUS, 0) # turn off autofocus
    print(autofocus)
    print(cap.get(cv2.CAP_PROP_AUTOFOCUS))


    axisPoints = np.array([[0,0,0],[length,0,0],[0,length,0],[0,0,length]])


    while cap.isOpened():
        flags, frame = cap.read()
        corners, ids, rejectedImgPoints = aruco.detectMarkers(frame, dictionary)
        
        new_image = None
        
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
                    if id == obj['id']:
                        obj = update_obj(obj, center, front)

        # print all objects ID/POSITION/ANGLE
        for (key, obj) in scene_objects.items():
            print_object_info(obj)

        claw_to_can_angle = get_claw_to_can_angle(frame, scene_objects)

        if count > 10:
            count = 0
        else:
            count += 1
            cv2.imshow('frame', frame)

            if claw_to_can_angle > 180:
                print('turn left')
            else:
                print('turn right')
            
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    print('cap closed, releasing and closing windows')        
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()

