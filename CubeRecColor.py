import cv2
import numpy as np

hmin, smin, vmin = 0, 0, 0
hmax, smax, vmax = 255, 255, 255

def nothing(x):
    pass

cv2.namedWindow("Trackbar", cv2.WINDOW_NORMAL)

cv2.createTrackbar("Hmin", "Trackbar", hmin, 255, nothing)
cv2.createTrackbar("Hmax", "Trackbar", hmax, 255, nothing)
cv2.createTrackbar("Smin", "Trackbar", smin, 255, nothing)
cv2.createTrackbar("Smax", "Trackbar", smax, 255, nothing)
cv2.createTrackbar("Vmin", "Trackbar", vmin, 255, nothing)
cv2.createTrackbar("Vmax", "Trackbar", vmax, 255, nothing)

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()

    src_img = frame
    hsv = cv2.cvtColor(src_img, cv2.COLOR_BGR2HSV)



    hmin = cv2.getTrackbarPos('Hmin', 'Trackbar')

    lower = np.array([hmin, smin, vmin])
    upper = np.array([hmax, smax, vmax])

    mask = cv2.inRange(hsv, lower, upper)

    hmin = cv2.getTrackbarPos('Hmin', 'Trackbar')
    hmax = cv2.getTrackbarPos('Hmax', 'Trackbar')
    smin = cv2.getTrackbarPos('Smin', 'Trackbar')
    smax = cv2.getTrackbarPos('Smax', 'Trackbar')
    vmin = cv2.getTrackbarPos('Vmin', 'Trackbar')
    vmax = cv2.getTrackbarPos('Vmax', 'Trackbar')

    cv2.imshow('img', frame)
    cv2.imshow('hsv', hsv)
    cv2.imshow('mask', mask)

    if cv2.waitKey(5) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
