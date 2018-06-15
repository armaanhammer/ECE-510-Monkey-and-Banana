# found at: https://gist.github.com/hauptmech/6b8ca2c05a3d935c97b1c75ec9ad85ff

import numpy as np
import cv2

import Arlib

cap = cv2.VideoCapture(0)

w = cap.get(3) # width
h = cap.get(4) # height

obj1 = [[499],[824],[585],[653],[193],[904]]
obj2 = [[913],[482],[737],[210],[654],[377],[833],[304],[849],[832],[728],[832]]
obj3 = [[  1],[  8],[932],[901],[131],[151],[871],[117],[ 66],[112],[427],[808]]


#dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_1000)
#dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_3X3_50)
#dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_ARUCO_ORIGINAL)
#print(dictionary)


Detected_ArUco_markers = {}
ArUco_marker_angles = {}

    
    
    


while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    # Arlib stuff
    Detected_ArUco_markers = Arlib.detect_ArUco(frame)
    ArUco_marker_angles = Arlib.Calculate_orientation_in_degree(Detected_ArUco_markers)
    img = Arlib.mark_ArUco(frame,Detected_ArUco_markers,ArUco_marker_angles)
    print(Detected_ArUco_markers)
    print(ArUco_marker_angles)
    
    
    

    # Our operations on the frame come here
#    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#    gray = frame

#    parameters =  cv2.aruco.DetectorParameters_create()
    #print(parameters)


#    corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(frame, dictionary, parameters=parameters)
#    if corners:
#        print("\nCorners:")
#        print(corners)
        
#    if ids.any() != None: # causes exception when NO markers are present:
#                          # AttributeError: 'NoneType' object has no attribute 'any'
#    if ids != None: # causes exception when AT LEAST ONE marker is present:
#                    # ValueError: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()
    
#        print("\nIDs:")
#        print(ids) # oh, duh. Just use corners as if for both.
#        print()
        
        
        
        
#    print("Rejects:")
#    print(len(rejectedImgPoints))
#    print(corners,ids,len(rejectedImgPoints))
#    print("-----")

#    res = cv2.aruco.detectMarkers(frame,dictionary,parameters=parameters)
#    print(res[0],res[1],len(res[2]))
    
    
    # rvec, tvec, _ = aruco.estimatePoseSingleMarkers(corners, markerLength, camera_matrix, dist_coeffs)
    #rvec, tvec, _ = aruco.estimatePoseSingleMarkers(res[0], , frame, )


    
    #vect = markerIds
    
    

#    if len(rejectedImgPoints) > 0:
#        cv2.aruco.drawDetectedMarkers(frame,corners,ids)
    # Display the resulting frame
    cv2.imshow('img',img)
    if cv2.waitKey(1000) & 0xFF == ord('q'): #wait 25ms
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
