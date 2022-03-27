import cv2
import numpy as np


def capture_rec(cap)




if __name__ == '__main__':
    mcap = cv2.VideoCapture(0)
    while True:
        img, ret = capture_rec(mcap)
        cv2.imshow("Video", img)
        if len(ret):
            print(ret)

        if cv2.waitKey(1) == ord("q"):
            break

    mcap.release()
    cv2.destroyAllWindows()
