import cv2
import numpy as np

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()

    src_img = frame
    hsv = cv2.cvtColor(src_img, cv2.COLOR_BGR2HSV)
    lower_red = np.array([0, 43, 46])
    upper_red = np.array([10, 255, 255])
    mask = cv2.inRange(hsv, lower_red, upper_red)

    cv2.imshow('hsv', mask)

    if cv2.waitKey(10) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
