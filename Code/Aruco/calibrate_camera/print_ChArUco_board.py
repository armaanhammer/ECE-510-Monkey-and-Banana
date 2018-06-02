import cv2
import cv2.aruco as aruco

dictionary = aruco.getPredefinedDictionary(aruco.DICT_ARUCO_ORIGINAL)
board = aruco.CharucoBoard_create(5, 7, 0.04, 0.02, dictionary)

img = board.draw((500,700))
cv2.imwrite('charuco.png', img)



