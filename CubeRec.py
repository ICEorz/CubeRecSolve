import functools

import cv2
import numpy as np


def capture_rec(cap):
    ret, frame = cap.read()

    src_img = frame
    roi_width = 300
    roi_height = 300
    width = frame.shape[1]
    height = frame.shape[0]
    margin_width = (width - roi_width) // 2
    margin_height = (height - roi_height) // 2
    roi = src_img[margin_height:margin_height + roi_height, margin_width: margin_width + roi_width]
    width = roi.shape[1]
    height = roi.shape[0]
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    blurred = cv2.GaussianBlur(blurred, (3, 3), 0)
    canny = cv2.Canny(blurred, 30, 50)

    kernel = np.ones((3, 3), np.uint8)
    dilated = cv2.dilate(canny, kernel, iterations=2)
    #
    dilated = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, kernel, anchor=(2, 0), iterations=3)

    contours, hierarchy = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    candidates = []
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.12 * cv2.arcLength(contour, True), True)
        area = cv2.contourArea(contour)
        if len(approx) == 4 and 2500 < area < 5000:
            xr, yr, wr, hr = cv2.boundingRect(contour)
            candidates.append((xr, yr, wr, hr))

    if len(candidates) != 9:
        for xx, yy, ww, hh in candidates:
            cv2.rectangle(roi, (xx, yy), (xx + ww, yy + hh), (255, 0, 0), 2)
        cv2.rectangle(src_img, (margin_width, margin_height), (margin_width + roi_width, margin_height + roi_height), (0, 0, 0), 2)
        return src_img, ''
    else:
        output = ''
        res_list = []

        for xx, yy, ww, hh in candidates:
            a = color_judge(hsv[yy:yy + hh, xx:xx + ww])
            res_list.append(ColorAndPosition(xx, yy, a))

        res_list = sorted(res_list, key=functools.cmp_to_key(cmp))
        for cp in res_list:
            # print(cp.x, cp.y, end='  ')
        # print()
            output += cp.color
        for xx, yy, ww, hh in candidates:
            cv2.rectangle(roi, (xx, yy), (xx + ww, yy + hh), (255, 0, 0), 2)
    cv2.rectangle(src_img, (margin_width, margin_height), (margin_width + roi_width, margin_height + roi_height), (0, 0, 0), 2)
    return src_img, output


def cmp(a, b):
    if abs(a.y - b.y) < 10:
        return a.x - b.x
    else:
        return a.y - b.y


def color_judge(color_img):
    lower_red = np.array([0, 43, 46])
    upper_red = np.array([10, 255, 255])

    lower_green = np.array([35, 43, 46])
    upper_green = np.array([77, 255, 255])

    lower_blue = np.array([100, 43, 46])
    upper_blue = np.array([124, 255, 255])

    lower_orange = np.array([11, 43, 46])
    upper_orange = np.array([25, 255, 255])

    lower_yellow = np.array([26, 43, 46])
    upper_yellow = np.array([50, 255, 255])

    lower_white = np.array([0, 0, 165])
    upper_white = np.array([182, 50, 255])

    red_hsv = cv2.inRange(color_img, lower_red, upper_red)
    green_hsv = cv2.inRange(color_img, lower_green, upper_green)
    blue_hsv = cv2.inRange(color_img, lower_blue, upper_blue)
    orange_hsv = cv2.inRange(color_img, lower_orange, upper_orange)
    yellow_hsv = cv2.inRange(color_img, lower_yellow, upper_yellow)
    white_hsv = cv2.inRange(color_img, lower_white, upper_white)

    # cv2.imshow('red', red_hsv)
    # cv2.imshow('green', green_hsv)
    # cv2.imshow('blue', blue_hsv)
    # cv2.imshow('orange', orange_hsv)
    # cv2.imshow('yellow', yellow_hsv)
    # cv2.imshow('white', white_hsv)

    twidth = color_img.shape[1]
    theight = color_img.shape[0]
    total_red = ColorCnt('R', 0)
    total_green = ColorCnt('B', 0)
    total_blue = ColorCnt('F', 0)
    total_orange = ColorCnt('L', 0)
    total_yellow = ColorCnt('U', 0)
    total_white = ColorCnt('D', 0)

    for i in range(theight):
        for j in range(twidth):
            if red_hsv[i, j] == 255:
                total_red.cnt += 1
            if green_hsv[i, j] == 255:
                total_green.cnt += 1
            if blue_hsv[i, j] == 255:
                total_blue.cnt += 1
            if orange_hsv[i, j] == 255:
                total_orange.cnt += 1
            if yellow_hsv[i, j] == 255:
                total_yellow.cnt += 1
            if white_hsv[i, j] == 255:
                total_white.cnt += 1
    res_list = [total_red, total_blue, total_white, total_yellow, total_orange, total_green]

    return sorted(res_list, key=lambda x: x.cnt, reverse=True)[0].name


class ColorCnt:
    def __init__(self, name, cnt):
        self.name = name
        self.cnt = cnt


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
        if len(ret):
            print(ret)

        if cv2.waitKey(5) == ord("q"):
            break

    mcap.release()
    cv2.destroyAllWindows()
