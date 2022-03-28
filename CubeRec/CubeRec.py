import functools
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import cv2
import numpy as np
import kociemba


# rec the color and convert it to string
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
        if len(approx) == 4 and 2000 < area < 5000:
            xr, yr, wr, hr = cv2.boundingRect(contour)
            candidates.append((xr, yr, wr, hr))

    if len(candidates) != 9:
        for xx, yy, ww, hh in candidates:
            cv2.rectangle(roi, (xx, yy), (xx + ww, yy + hh), (255, 0, 0), 2)
        draw_roi(src_img)
        return src_img, ''
    else:
        output = ''
        res_list = []

        for xx, yy, ww, hh in candidates:
            a = color_judge(hsv[yy:yy + hh, xx:xx + ww])
            res_list.append(ColorAndPosition(xx, yy, a))

        res_list = sorted(res_list, key=functools.cmp_to_key(cmp))
        for cp in res_list:
            output += cp.color
        for xx, yy, ww, hh in candidates:
            cv2.rectangle(roi, (xx, yy), (xx + ww, yy + hh), (255, 0, 0), 2)
    draw_roi(src_img)
    return src_img, output


# inorder to sort the rectangles
def cmp(a, b):
    if abs(a.y - b.y) < 10:
        return a.x - b.x
    else:
        return a.y - b.y


# judge which color it is
def color_judge(color_img):
    lower_red = np.array([0, 43, 46])
    upper_red = np.array([10, 255, 255])

    lower_green = np.array([50, 43, 46])
    upper_green = np.array([77, 255, 255])

    lower_blue = np.array([100, 43, 46])
    upper_blue = np.array([124, 255, 255])

    lower_orange = np.array([11, 43, 46])
    upper_orange = np.array([25, 255, 255])

    lower_yellow = np.array([26, 43, 46])
    upper_yellow = np.array([50, 255, 255])

    lower_white = np.array([0, 0, 165])
    upper_white = np.array([182, 50, 255])

    def color_fit(color, lower, upper):
        flag = True
        for j in lower <= color:
            flag &= j
        for j in color <= upper:
            flag &= j
        return flag

    twidth = color_img.shape[1]
    theight = color_img.shape[0]
    total_cnt = 0
    color = np.array([0, 0, 0])

    for i in range(theight // 4, theight * 3 // 4):
        for j in range(twidth // 4, twidth * 3 // 4):
            color += color_img[i, j]
            total_cnt += 1

    res_color = color // total_cnt

    if color_fit(res_color, lower_red, upper_red):
        return 'R'
    elif color_fit(res_color, lower_green, upper_green):
        return 'B'
    elif color_fit(res_color, lower_blue, upper_blue):
        return 'F'
    elif color_fit(res_color, lower_orange, upper_orange):
        return 'L'
    elif color_fit(res_color,lower_yellow, upper_yellow):
        return 'U'
    elif color_fit(res_color, lower_white, upper_white):
        return 'D'
    else:
        return ''


class ColorCnt:
    def __init__(self, name, cnt):
        self.name = name
        self.cnt = cnt


class ColorAndPosition:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color


# URFDLB
class Cube:
    def __init__(self):
        self.yellow_str = ''
        self.red_str = ''
        self.blue_str = ''
        self.white_str = ''
        self.orange_str = ''
        self.green_str = ''

    def output_string(self):
        return self.yellow_str + self.red_str + self.blue_str + self.white_str + self.orange_str + self.green_str

    def check(self):
        if len(self.yellow_str) != 0 and \
            len(self.red_str) != 0 and \
            len(self.blue_str) != 0 and \
            len(self.green_str) != 0 and \
            len(self.orange_str) != 0 and \
                len(self.white_str) != 0:
            return True
        else:
            return False

    def state(self):
        res = ''
        if len(self.yellow_str) == 0:
            res += '0'
        else:
            res += '1'
        if len(self.red_str) == 0:
            res += '0'
        else:
            res += '1'
        if len(self.blue_str) == 0:
            res += '0'
        else:
            res += '1'
        if len(self.white_str) == 0:
            res += '0'
        else:
            res += '1'
        if len(self.orange_str) == 0:
            res += '0'
        else:
            res += '1'
        if len(self.green_str) == 0:
            res += '0'
        else:
            res += '1'
        return res


class NowStr:
    def __init__(self, now_str):
        self.now_str = now_str



def draw_roi(img):
    cv2.line(img, (170, 90), (210, 90), (255, 255, 255), 3)
    cv2.line(img, (170, 90), (170, 130), (255, 255, 255), 3)
    cv2.line(img, (470, 90), (430, 90), (255, 255, 255), 3)
    cv2.line(img, (470, 90), (470, 130), (255, 255, 255), 3)
    cv2.line(img, (170, 390), (210, 390), (255, 255, 255), 3)
    cv2.line(img, (170, 390), (170, 350), (255, 255, 255), 3)
    cv2.line(img, (470, 390), (430, 390), (255, 255, 255), 3)
    cv2.line(img, (470, 390), (470, 350), (255, 255, 255), 3)


def video_loop():
    img, ret = capture_rec(mcap)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
    nowstr.now_str = ret
    current_img = Image.fromarray(img)
    imgtk = ImageTk.PhotoImage(image=current_img)
    panel.imgtk = imgtk
    panel.config(image=imgtk)
    root.after(1, video_loop)
    return ret


def take():
    ori_str = nowstr.now_str
    if len(ori_str) != 9:
        return
    if ori_str[4] == 'R':
        cube.red_str = ori_str
    elif ori_str[4] == 'L':
        cube.orange_str = ori_str
    elif ori_str[4] == 'U':
        cube.yellow_str = ori_str
    elif ori_str[4] == 'D':
        cube.white_str = ori_str
    elif ori_str[4] == 'B':
        cube.green_str = ori_str
    elif ori_str[4] == 'F':
        cube.blue_str = ori_str
    print(ori_str)


def solve():
    global cube
    if cube.check():
        print(cube.output_string())
        print(kociemba.solve(cube.output_string()))
        cube = Cube()
    else:
        print(cube.state())
        print('rec unfinished')


if __name__ == '__main__':
    mcap = cv2.VideoCapture(0)
    root = Tk()
    root.title('CubeRecSolve')
    cube = Cube()
    nowstr = NowStr('')
    panel = Label(root)
    panel.pack(padx=10, pady=10)
    root.config(cursor="arrow")
    btn = Button(root, text='REC', command=take)
    btn.pack(fill='both', expand=True, padx=10, pady=10)
    btn1 = Button(root, text='cal', command=solve)
    btn1.pack(fill='both', expand=True, padx=10, pady=10)

    video_loop()

    root.mainloop()

    mcap.release()
    cv2.destroyAllWindows()