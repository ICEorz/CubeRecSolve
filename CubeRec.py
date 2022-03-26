import functools

import cv2
import numpy as np


def capture_rec(cap):
    ret, frame = cap.read()

    src_img = frame
    hsv = cv2.cvtColor(src_img, cv2.COLOR_RGB2HSV)
    width = frame.shape[1]
    height = frame.shape[0]

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
        res_list = []
        total_h, total_s, total_v, total_amount = 0, 0, 0, 0
        for xx, yy, ww, hh in candidates:
            for i in range(max(0, xx), min(xx + ww, width)):
                for j in range(max(0, yy), min(yy + hh, height)):
                    total_amount += 1
                    try:
                        total_h += hsv[i, j][0]
                        total_s += hsv[i, j][1]
                        total_v += hsv[i, j][2]
                    finally:
                        continue

            color = np.array([int(total_h / total_amount), int(total_s / total_amount), int(total_v / total_amount)])
            # res_list.append(ColorAndPosition(xx, yy, color_judge(color)))
            res_list.append(ColorAndPosition(xx, yy, str(color) + ' '))

        sorted(res_list, key=functools.cmp_to_key(cmp))
        for cp in res_list:
            output += cp.color

    return src_img, output


def cmp(a, b):
    if abs(a.y - b.y) < 20:
        return a.x < b.x
    else:
        return a.y < b.y


def color_judge(color):
    lower_red = np.array([0, 43, 46])
    upper_red = np.array([10, 255, 255])
    lower_green = np.array([35, 43, 46])
    upper_green = np.array([77, 255, 255])
    lower_blue = np.array([100, 43, 46])
    upper_blue = np.array([124, 255, 255])
    lower_orange = np.array([11, 43, 46])
    upper_orange = np.array([25, 255, 255])
    lower_yellow = np.array([26, 43, 46])
    upper_yellow = np.array([34, 255, 255])
    lower_white = np.array([0, 0, 221])
    upper_white = np.array([180, 30, 255])

    def color_cmp(color1, lower, upper):
        lower_judge = color1 >= lower
        upper_judge = color1 <= upper
        flag = True
        for i in lower_judge:
            flag &= i
        for i in upper_judge:
            flag &= i
        return i

    if color_cmp(color, lower_red, upper_red):
        return 'R'
    elif color_cmp(color, lower_yellow, upper_yellow):
        return 'U'
    elif color_cmp(color, lower_green, upper_green):
        return 'B'
    elif color_cmp(color, lower_blue, upper_blue):
        return 'F'
    elif color_cmp(color, lower_white, upper_white):
        return 'D'
    elif color_cmp(color, lower_orange, upper_orange):
        return 'L'
    else:
        return ''


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
        print(ret)

        if cv2.waitKey(5) == ord("q"):
            break

    mcap.release()
    cv2.destroyAllWindows()