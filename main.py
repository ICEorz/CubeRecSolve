import tkinter as tk
import kociemba
import cv2
from PIL import Image, ImageTk
import CubeRec
import DrawCube
from tkinter import messagebox
import tkinter.font as font


class Cube(CubeRec.Cube, DrawCube.Cube):
    def __init__(self):
        DrawCube.Cube.__init__(self)
        CubeRec.Cube.__init__(self)
        self.state_list = ['U', 'R', 'F', 'D', 'L', 'B']
        self.state_to_idx = {
            'U': 0,
            'R': 1,
            'F': 2,
            'D': 3,
            'L': 4,
            'B': 5
        }
        self.state_to_color = {
            'U': 'yellow',
            'R': 'red',
            'F': 'blue',
            'D': 'white',
            'L': 'orange',
            'B': 'green'
        }
        self.color_to_state = {
            'yellow': 'U',
            'red': 'R',
            'blue': 'F',
            'white': 'D',
            'orange': 'L',
            'green': 'B'
        }

    def color_to_frame(self, color_string):
        if len(color_string) != 9:
            return

        for i in range(9):
            self.select_idx = self.state_to_idx[color_string[i]]
            self.change_color(self.state_to_color[color_string[4]] + ' ' + str(i))

    def change_color(self, name_str):
        super().change_color(name_str)
        name_str, idx = name_str.split()
        idx = int(idx)

        def convert(color_str):
            con_list = list(color_str)
            if len(con_list) == 9:
                con_list[idx] = self.state_list[self.select_idx]
            return ''.join(con_list)

        if name_str == 'red':
            convert(self.red_str)
        if name_str == 'green':
            convert(self.green_str)
        if name_str == 'blue':
            convert(self.blue_str)
        if name_str == 'orange':
            convert(self.orange_str)
        if name_str == 'white':
            convert(self.white_str)
        if name_str == 'yellow':
            convert(self.yellow_str)

    def clear(self):
        self.yellow_str = ''
        self.red_str = ''
        self.blue_str = ''
        self.white_str = ''
        self.green_str = ''
        self.orange_str = ''

        def clear_side(side):
            for si in side:
                si.config(background='white')

        clear_side(self.red_side)
        clear_side(self.yellow_side)
        clear_side(self.blue_side)
        clear_side(self.orange_side)
        clear_side(self.green_side)
        clear_side(self.white_side)


def video_loop():
    img, ret = CubeRec.capture_rec(mframe)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
    now_str.now_str = ret
    current_img = Image.fromarray(img)
    img_tk = ImageTk.PhotoImage(image=current_img)
    panel.img_tk = img_tk
    panel.config(image=img_tk)


def take():
    ori_str = now_str.now_str
    if len(ori_str) != 9:
        return
    if ori_str[4] == 'R':
        magic_cube.red_str = ori_str
    elif ori_str[4] == 'L':
        magic_cube.orange_str = ori_str
    elif ori_str[4] == 'U':
        magic_cube.yellow_str = ori_str
    elif ori_str[4] == 'D':
        magic_cube.white_str = ori_str
    elif ori_str[4] == 'B':
        magic_cube.green_str = ori_str
    elif ori_str[4] == 'F':
        magic_cube.blue_str = ori_str
    magic_cube.color_to_frame(ori_str)


def solve():
    global magic_cube
    if magic_cube.check():
        messagebox.showinfo('Solution', kociemba.solve(magic_cube.output_string()))
    else:
        messagebox.showerror('Error', 'Recognition unfinished')


class NowStr:
    def __init__(self, ss):
        self.now_str = ss


if __name__ == '__main__':
    mcap = cv2.VideoCapture(0)
    root = tk.Tk()
    root.title('CubeRecSolve')
    magic_cube = Cube()
    cube_state = tk.Toplevel()
    cube_state.geometry('640x480')

    v = tk.IntVar()
    v.set(0)

    pixel_image = tk.PhotoImage(width=1, height=1)

    select_frame = tk.Frame(cube_state, width=20, height=120)
    cube_frame = tk.Frame(cube_state, padx=25, pady=30)
    select_frame.grid(row=0, column=0)
    cube_frame.grid(row=0, column=1)

    magic_cube.generate_frames(cube_frame)


    def set_cube_color():
        magic_cube.select_idx = v.get()


    tk.Radiobutton(select_frame, image=pixel_image, variable=v, value=0, indicatoron=False, background='yellow',
                   selectcolor='yellow', width=20, height=20, compound='center', command=set_cube_color).pack()
    tk.Radiobutton(select_frame, image=pixel_image, variable=v, value=1, indicatoron=False, background='red',
                   selectcolor='red', width=20, height=20, compound='center', command=set_cube_color).pack()
    tk.Radiobutton(select_frame, image=pixel_image, variable=v, value=2, indicatoron=False, background='blue',
                   selectcolor='blue', width=20, height=20, compound='center', command=set_cube_color).pack()
    tk.Radiobutton(select_frame, image=pixel_image, variable=v, value=3, indicatoron=False, background='white',
                   selectcolor='white', width=20, height=20, compound='center', command=set_cube_color).pack()
    tk.Radiobutton(select_frame, image=pixel_image, variable=v, value=4, indicatoron=False, background='orange',
                   selectcolor='orange', width=20, height=20, compound='center', command=set_cube_color).pack()
    tk.Radiobutton(select_frame, image=pixel_image, variable=v, value=5, indicatoron=False, background='green',
                   selectcolor='green', width=20, height=20, compound='center', command=set_cube_color).pack()

    clear_btn = tk.Button(select_frame, text='AC', command=magic_cube.clear, font=font.Font(size=15))
    clear_btn.pack()

    now_str = NowStr('')
    panel = tk.Label(root)
    panel.pack(padx=10, pady=10)
    root.config(cursor="arrow")
    btn = tk.Button(root, text='REC', command=take)
    btn.pack(fill='both', expand=True, padx=10, pady=10)
    btn1 = tk.Button(root, text='cal', command=solve)
    btn1.pack(fill='both', expand=True, padx=10, pady=10)

    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            mcap.release()
            cv2.destroyAllWindows()
            root.destroy()

    root.protocol('WM_DELETE_WINDOW', on_closing)

    while True:
        st, mframe = mcap.read()
        video_loop()
        root.update()
        root.after(10)