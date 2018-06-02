import numpy as np
import cv2
import cv2.aruco as aruco
import time
import yaml


dictionary = aruco.getPredefinedDictionary(aruco.DICT_ARUCO_ORIGINAL)
board = aruco.CharucoBoard_create(5, 7, 0.04, 0.02, dictionary)

img = board.draw((500,700))
cv2.imwrite('charuco.png', img)

cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_AUTOFOCUS, 0) # turn off autofocus

allCorners = []
allIds = []
decimator = 0

for i in range(300):
# while cap.isOpened():
    flags, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    res = aruco.detectMarkers(gray, dictionary)
    if len(res[0])>0:
        print('Detected markers')
        res2 = aruco.interpolateCornersCharuco(res[0], res[1], gray, board)
        if res2[1] is not None and \
           res2[2] is not None and \
           len(res2[1])>3 and \
           decimator%3==0:
            print('Found Corners and IDs')
            allCorners.append(res2[1])
            allIds.append(res2[2])

            aruco.drawDetectedMarkers(gray, res[0], res[1])
        
    cv2.imshow('frame', gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    decimator += 1

imsize = gray.shape	

print(allCorners)
print(allIds)  
print(imsize)

d = {
	'allCorners': allCorners,
	'allIds': allIds,
	'imsize': imsize
}

with open('result.yml', 'w') as yaml_file:
    yaml.dump(d, yaml_file, default_flow_style=False)
	


# Calibration fails for lots of reasons.  Release the video if we do
# try:
#     cal = aruco.calibrateCameraCharuco(allCorners, allIds, board, imsize, None, None)
#     print('Successfully calibrated the camera!!!')
# except:
#     print('ERROR: Could not calibrate camera')
#     cap.release()
        
cap.release()
cv2.destroyAllWindows()