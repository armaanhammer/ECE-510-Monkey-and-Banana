import cv2
import cv2.aruco as aruco
from random import randint


size = 100
num_markers = 5
ids = []

dictionary = aruco.getPredefinedDictionary(aruco.DICT_ARUCO_ORIGINAL)

for i in range(num_markers):
    id_not_unique = True
    id = None
    while id_not_unique:
        id = randint(1, len(dictionary.bytesList) + 1)
        if id not in ids:
            id_not_unique = False
            ids.append(id)
            
    img = aruco.drawMarker(dictionary, id, size)
    img_name = 'aruco_{}.png'.format(id)
    cv2.imwrite(img_name, img)
    
    
# img = aruco.drawMarker(dictionary, 1, 100)
# cv2.imwrite('aruco_1.png', img)

# img = aruco.drawMarker(dictionary, 23, 100)
# cv2.imwrite('aruco_2.png', img)

# img = aruco.drawMarker(dictionary, 3, 100)
# cv2.imwrite('aruco_3.png', img)

# img = aruco.drawMarker(dictionary, 4, 100)
# cv2.imwrite('aruco_4.png', img)

# img = aruco.drawMarker(dictionary, 5, 100)
# cv2.imwrite('aruco_5.png', img)