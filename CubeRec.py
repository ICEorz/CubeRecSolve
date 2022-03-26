import functools

import cv2
import numpy as np


def capture_rec(cap):
    ret, frame = cap.read()

    src_img = frame
    gray = cv2.cvtColor(src_img, cv2.COLOR_BGR2GRAY)

    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    canny = cv2.Canny(blurred, 20, 40)

    kernel = np.ones((3, 3), np.uint8)
    dilated = cv2.dilate(canny, kernel, iterations=2)
    #
    dilated = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, kernel, anchor=(2, 0), iterations=2)

    contours, hierarchy = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    candidates = []
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.13 * cv2.arcLength(contour, True), True)
        area = cv2.contourArea(contour)
        if len(approx) == 4 and 2500 < area < 5000:
            xr, yr, wr, hr = cv2.boundingRect(contour)
            candidates.append((xr, yr, wr, hr))
            cv2.rectangle(src_img, (xr, yr), (xr + wr, yr + hr), (255, 0, 0), 2)

    if len(candidates) != 9:
        return src_img, ''
    else:
        output = ''
        print(candidates)
        sorted(candidates, key=functools.cmp_to_key(cmp))

        total_red, total_green, total_blue, total_amount = 0, 0, 0, 0
        for xx, yy, ww, hh in candidates:
            for i in range(xx, xx + ww // 2):
                for j in range(yy, yy + hh // 2):
                    total_amount += 1
                    total_red += src_img[i, j][2]
                    total_green += src_img[i, j][1]
                    total_blue += src_img[i, j][0]


    return src_img, output


def cmp(a, b):
    if abs(a.y - b.y) < 20:
        return a.x < b.x
    else:
        return a.y < b.y


def color_judge(color):
    red = (155, 30, 30)
    green = (5, 150, 30)
    yellow = (140, 160, 40)


class ColorAndPosition:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color


if __name__ == '__main__':
    mcap = cv2.VideoCapture(0)
    while True:
        img, ret = capture_rec(mcap)
        cv2.imshow("Video", img)

        if cv2.waitKey(10) == ord("q"):
            break

    mcap.release()
    cv2.destroyAllWindows()