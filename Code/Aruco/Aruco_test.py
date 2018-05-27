# found at: https://gist.github.com/hauptmech/6b8ca2c05a3d935c97b1c75ec9ad85ff

import numpy as np
import cv2

cap = cv2.VideoCapture(0)

w = cap.get(3) # witch
h = cap.get(4) # height

#dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_1000)
#dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_3X3_50)
#dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_ARUCO_ORIGINAL)


while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
#    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#    gray = cv2.cvtColor(frame, cv2.COLOR)
    gray = frame

    res = cv2.aruco.detectMarkers(gray,dictionary)
    print(res[0],res[1],len(res[2]))
    
    
    
    #vect = markerIds
    
    

    if len(res[0]) > 0:
        cv2.aruco.drawDetectedMarkers(gray,res[0],res[1])
    # Display the resulting frame
    cv2.imshow('frame',gray)
    if cv2.waitKey(25) & 0xFF == ord('q'): #wait 25ms
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
