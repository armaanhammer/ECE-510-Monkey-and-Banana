import numpy as np
import cv2
import cv2.aruco as aruco
import time
import yaml


with open('camera_calibration_results.yml', 'r') as yaml_file:
    d = yaml.load(yaml_file)

retval = d['retval']
cameraMatrix = d['cameraMatrix']
distCoeffs = d['distCoeffs']
rvecs_orig = d['rvecs']
tvecs_orig = d['tvecs']

dictionary = aruco.getPredefinedDictionary(aruco.DICT_ARUCO_ORIGINAL)

cap = cv2.VideoCapture(1)
# cap.set(cv2.CAP_PROP_AUTOFOCUS, 0) # turn off autofocus
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
cap.set(cv2.CAP_PROP_SETTINGS, 1)

print(cap.get(cv2.CAP_PROP_AUTOFOCUS))

count = 0
while cap.isOpened():
    flags, frame = cap.read()
    corners, ids, rejectedImgPoints = aruco.detectMarkers(frame, dictionary)
    
    new_image = None
    
    if len(corners)>0:
        # print('Detected markers')
        
        aruco.drawDetectedMarkers(frame, corners, ids)
        
        rvecs, tvecs, obj_points = aruco.estimatePoseSingleMarkers(corners, 0.04, cameraMatrix, distCoeffs)
        
        for rvec, tvec in zip(rvecs, tvecs):
            aruco.drawAxis(frame, cameraMatrix, distCoeffs, rvec, tvec, 0.04)

    if count > 10:
        count = 0
    else:
        cv2.imshow('frame', frame)
        count += 1            
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        
    
        
cap.release()
cv2.destroyAllWindows()