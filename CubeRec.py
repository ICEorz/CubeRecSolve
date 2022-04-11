import functools
import cv2
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk
import threading

# recognize the cube
def capture_rec(frame):
    src_img = frame
    roi_width = 300
    roi_height = 300
    width = frame.shape[1]
    height = frame.shape[0]
    margin_width = (width - roi_width) // 2
    margin_height = (height - roi_height) // 2
    roi = src_img[margin_height:margin_height + roi_height, margin_width: margin_width + roi_width]

    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    canny = cv2.Canny(blurred, 30, 50)

    kernel = np.ones((3, 3), np.uint8)
    dilated = cv2.dilate(canny, kernel, iterations=2)
    
    dilated2 = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, kernel, anchor=(2, 0), iterations=3)

    contours, hierarchy = cv2.findContours(dilated2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    candidates = []
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.12 * cv2.arcLength(contour, True), True)
        area = cv2.contourArea(contour)
        if len(approx) == 4 and 2000 < area < 6000:
            xr, yr, wr, hr = cv2.boundingRect(contour)
            candidates.append((xr, yr, wr, hr))
    
    def draw_roi(img):
        cv2.line(img, (170, 90), (210, 90), (255, 255, 255), 3)
        cv2.line(img, (170, 90), (170, 130), (255, 255, 255), 3)
        cv2.line(img, (470, 90), (430, 90), (255, 255, 255), 3)
        cv2.line(img, (470, 90), (470, 130), (255, 255, 255), 3)
        cv2.line(img, (170, 390), (210, 390), (255, 255, 255), 3)
        cv2.line(img, (170, 390), (170, 350), (255, 255, 255), 3)
        cv2.line(img, (470, 390), (430, 390), (255, 255, 255), 3)
        cv2.line(img, (470, 390), (470, 350), (255, 255, 255), 3)

    for xx, yy, ww, hh in candidates:
        cv2.rectangle(roi, (xx, yy), (xx + ww, yy + hh), (255, 0, 0), 2)
    draw_roi(src_img)

    return src_img, candidates

def color_rec(img, candidates):
    if len(candidates) != 9:
        return ''
    else:
        output = ''
        res_list = []
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        for xx, yy, ww, hh in candidates:
            a = color_judge(hsv[yy:yy + hh, xx:xx + ww])
            res_list.append(ColorAndPosition(xx, yy, a))

        res_list = sorted(res_list, key=functools.cmp_to_key(cmp))
        for cp in res_list:
            output += cp.color
    return output


# inorder to sort the rectangles
def cmp(a, b):
    if abs(a.y - b.y) < 15:
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

    def color_fit(fitting_color: np.array, lower: np.array, upper: np.array):
        flag = True
        for judge in lower <= fitting_color:
            flag &= judge
        for judge in fitting_color <= upper:
            flag &= judge
        return flag

    # calculate the average hsv
    t_width = color_img.shape[1]
    t_height = color_img.shape[0]
    total_cnt = 0
    color = np.array([0, 0, 0])

    for i in range(t_height // 4, t_height * 3 // 4):
        for j in range(t_width // 4, t_width * 3 // 4):
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
    elif color_fit(res_color, lower_yellow, upper_yellow):
        return 'U'
    elif color_fit(res_color, lower_white, upper_white):
        return 'D'
    else:
        return ''

class ColorAndPosition:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color


# U R F D L B
class Cube:
    def __init__(self):
        self.YELLOW = 0
        self.RED = 1
        self.BLUE = 2
        self.WHITE = 3
        self.ORANGE = 4
        self.GREEN = 5
        self.str_list = ['' for x in range(6)]


    def output_string(self):
        return self.str_list.join('')

    def check(self):
        if len(self.output_string()) != 0:
            return True
        else:
            return False

def rec():
    print('taking')


def video_loop():
    root = tk.Tk()
    root.geometry('640x480')
    panel = tk.Label(root)
    panel.pack(padx=10, pady=10)
    btn = tk.Button(root, text="rec", command=rec)
    btn.pack(padx=10, pady=10)
    cap = cv2.VideoCapture(0)
    while True: 
        ref, frame = cap.read()
        cvimage, candidates = capture_rec(frame)
        cvimage = cv2.cvtColor(cvimage, cv2.COLOR_BGR2RGBA)
        current_img = Image.fromarray(cvimage)
        img_tk = ImageTk.PhotoImage(image=current_img)
        panel.img_tk = img_tk
        panel.config(image=img_tk)
        root.update()
        root.after(1)


if __name__ == '__main__':
    video_thread = threading.Thread(target=video_loop)
    video_thread.start()
    # video_loop()


