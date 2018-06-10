import numpy as np
import cv2
import cv2.aruco as aruco
from pprint import pprint
import time
import yaml

length = 0.04 # length of marker side
count = 0
max_count = 10

CAN_ID = 880
CLAW_ROBOT_ID = 481

can = {
    'id': CAN_ID,
}

claw_robot = {
    'id': CLAW_ROBOT_ID,
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
            
(retval, cameraMatrix, distCoeffs, rvecs_orig, tvecs_orig) = read_calibration_data('camera_calibration_results.yml')

dictionary = aruco.getPredefinedDictionary(aruco.DICT_ARUCO_ORIGINAL)

cap = cv2.VideoCapture(0)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 720)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# cap.set(cv2.CAP_PROP_SETTINGS, 1)

# is it set correctly?
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)

# wtf autofocus?
autofocus = cap.set(cv2.CAP_PROP_AUTOFOCUS, 0) # turn off autofocus
print(autofocus)
print(cap.get(cv2.CAP_PROP_AUTOFOCUS))


axisPoints = np.array([[0,0,0],[length,0,0],[0,length,0],[0,0,length]])

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

    # if angle >= 180:
    #     angle = angle - 180
    # else:
    #     angle = angle + 180
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

while cap.isOpened():
  
  
    flags, frame = cap.read()
    corners, ids, rejectedImgPoints = aruco.detectMarkers(frame, dictionary)
    
    new_image = None
    
    if len(corners)>0:
        # print('Detected markers')
        
        centers_calc = find_all_centers(corners)
        # print(10*'-')
        # print(centers)
        # print(10*'-')

        # draw_centers(frame, centers)

        # aruco.drawDetectedMarkers(frame, corners, ids)
        
        rvecs, tvecs, obj_points = aruco.estimatePoseSingleMarkers \
        (corners, length, cameraMatrix, distCoeffs)
        
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
            # print(10*'-')
            # print('ID:\t{}'.format(id))
            if id == CAN_ID:
                # print('Found the can!!!')
                can['position'] = center
                can['front'] = front
                can['angle'] = get_angle(center, front)

            elif id == CLAW_ROBOT_ID:
                # print('Found the claw robot!!!')
                claw_robot['position'] = center
                claw_robot['front'] = front
                claw_robot['angle'] = get_angle(center, front)
            else:
                print('Found an unknown object with ID: {}'.format(id))
                
            # print('Center:\t({}, {})'.format(center[0], center[1]))
            # print('Front:\t({}, {})'.format(front[0], front[1]))
            # print(10*'-')
            # print()
            

    print(10*'-')
    if 'id' in can.keys():
        print('{} ID: {}'.format('CAN', can['id']))

    if 'position' in can.keys():
        print('{} position: {}'.format('CAN', can['position']))

    if 'angle' in can.keys():
        print('{} angle: {}'.format('CAN', can['angle']))

    print(10*'-')

    if 'id' in claw_robot.keys():
        print('{} ID: {}'.format('CLAW', claw_robot['id']))

    if 'position' in claw_robot.keys():
        print('{} position: {}'.format('CLAW', claw_robot['position']))

    if 'angle' in claw_robot.keys():
        print('{} angle: {}'.format('CLAW', claw_robot['angle']))

    print(10*'-')

    if count > 10:
        count = 0
    else:
        cv2.imshow('frame', frame)
        count += 1
   
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        
    
    
print('cap closed, releasing and closing windows')        
cap.release()
cv2.destroyAllWindows()
