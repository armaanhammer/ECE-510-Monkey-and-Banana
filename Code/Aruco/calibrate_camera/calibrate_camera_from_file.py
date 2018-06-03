import numpy as np
import cv2
import cv2.aruco as aruco
import time
import yaml

# Input:    yaml.load

# Outputs:  camera_calibration_results.yml  <  contains all data
#           camera_matrix.yml               <  contains on cameraMatrix

with open('result.yml', 'r') as yaml_file:
    d = yaml.load(yaml_file)

dictionary = aruco.getPredefinedDictionary(aruco.DICT_ARUCO_ORIGINAL)
board = aruco.CharucoBoard_create(5, 7, 0.04, 0.02, dictionary) 
    
allCorners = d['allCorners']
allIds = d['allIds']
imsize = d['imsize']

# Calibration fails for lots of reasons.  Release the video if we do
try:
    print('Starting calibration')
    cal = aruco.calibrateCameraCharuco(allCorners, allIds, board, imsize, None, None)
    print('Successfully calibrated the camera!!!')
    
    retval, cameraMatrix, distCoeffs, rvecs, tvecs = cal
    
    d = {
        'retval': retval,
        'cameraMatrix': cameraMatrix,
        'distCoeffs': distCoeffs,
        'rvecs': rvecs,
        'tvecs': tvecs
    }
    
    print(cameraMatrix)
    
    with open('camera_calibration_results.yml', 'w') as yaml_file:
        yaml.dump(d, yaml_file, default_flow_style=False)
        
    with open('camera_matrix.yml', 'w') as yaml_file:
        yaml.dump(cameraMatrix, yaml_file, default_flow_style=False)
        
except:
    print('ERROR: Could not calibrate camera')