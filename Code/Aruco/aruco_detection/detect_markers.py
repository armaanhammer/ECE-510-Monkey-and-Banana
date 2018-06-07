import numpy as np
import cv2
import cv2.aruco as aruco
import time
import yaml
import matplotlib.pyplot as plt

length = 0.04 # length of marker side
count = 0

objLocations = [[]]


with open('camera_calibration_results.yml', 'r') as yaml_file:
    d = yaml.load(yaml_file)

retval = d['retval']
cameraMatrix = d['cameraMatrix']
distCoeffs = d['distCoeffs']
rvecs_orig = d['rvecs']
tvecs_orig = d['tvecs']

dictionary = aruco.getPredefinedDictionary(aruco.DICT_ARUCO_ORIGINAL)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
cap.set(cv2.CAP_PROP_SETTINGS, 1)

# is it set correctly?
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)

# wtf autofocus?
autofocus = cap.set(cv2.CAP_PROP_AUTOFOCUS, 0) # turn off autofocus
print(autofocus)
print(cap.get(cv2.CAP_PROP_AUTOFOCUS))


axisPoints = np.array([[0,0,0],[length,0,0],[0,length,0],[0,0,length]])


def find_center(cnrs):
    x = cnrs[0][0][0] + cnrs[0][1][0] + cnrs[0][2][0] + cnrs[0][3][0]
    x = x/4
    print(x)
    y = cnrs[0][0][1] + cnrs[0][1][1] + cnrs[0][2][1] + cnrs[0][3][1]
    y = y/4
    print(y)
    return([x,y])
  
  
def find_front(crns):
  pass



fig = plt.figure(figsize=(8,8))
ax = fig.add_axes([0.05,0.05,0.92,0.92])
#ax.set_xlim(-6,6)
#ax.set_ylim(-6,6)
scale = 0.2
X,Y=np.mgrid[-5:5:scale, -5:5:scale]


while cap.isOpened():
  
  
    flags, frame = cap.read()
    corners, ids, rejectedImgPoints = aruco.detectMarkers(frame, dictionary)
    
    new_image = None
    
    if len(corners)>0:
        # print('Detected markers')
        
        aruco.drawDetectedMarkers(frame, corners, ids)
        
        rvecs, tvecs, obj_points = aruco.estimatePoseSingleMarkers \
        (corners, length, cameraMatrix, distCoeffs)
        
        i=0
        for rvec, tvec in zip(rvecs, tvecs):
            aruco.drawAxis(frame, cameraMatrix, distCoeffs, rvec, tvec, length)
            
            # Populate object locations
            imgPoints, _ = cv2.projectPoints(axisPoints, rvec, tvec, cameraMatrix, distCoeffs)
            objLocations[i] = [imgPoints[0][0][0],imgPoints[0][0][1]], \
                              [imgPoints[1][0][0],imgPoints[1][0][1]]
            test = np.array(objLocations)
            print('reached here')
            i = i+1
            
            print(test)
            


# =============================================================================
#         print(imagePoints)
#         print('_____________')
#         for cornVar in corners:
#           find_center
#         
#         for var in len(corners)
#         find_center(corners[0])
#         # print(obj_points)
# =============================================================================


    if count > 10:
        count = 0
    else:
        cv2.imshow('frame', frame)
        count += 1
        
        ax.quiver([0], [0], test[:,0], test[:,1])
        #plt.xlim(0, width)
        #plt.ylim(0, height)
        #plt.show('test', test)
        plt.show()
    
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        
    
    
        
cap.release()
cv2.destroyAllWindows()
