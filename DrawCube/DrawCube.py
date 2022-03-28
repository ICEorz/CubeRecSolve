import tkinter as tk


def cube_win():
    cube_state = tk.Tk()
    cube_state.geometry('640x480')
    v = tk.IntVar()

    v.set(0)

    blue_color = '#0000FF'
    red_color = '#FF0000'
    yellow_color = '#FFF61D'
    white_color = '#FFFFFF'
    green_color = '#22C900'
    orange_color = '#FFA10D'

    pixel_image = tk.PhotoImage(width=1, height=1)

    select_frame = tk.Frame(cube_state, width=20, height=120)
    cube_frame = tk.Frame(cube_state, padx=25, pady=30)
    select_frame.grid(row=0, column=0)
    cube_frame.grid(row=0, column=1)

    red_frame = tk.Frame(cube_frame)
    blue_frame = tk.Frame(cube_frame)
    yellow_frame = tk.Frame(cube_frame)
    white_frame = tk.Frame(cube_frame)
    green_frame = tk.Frame(cube_frame)
    orange_frame = tk.Frame(cube_frame)

    blue_frame.grid(row=1, column=1)
    orange_frame.grid(row=1, column=0)
    red_frame.grid(row=1, column=2)
    green_frame.grid(row=1, column=3)
    yellow_frame.grid(row=0, column=1)
    white_frame.grid(row=2, column=1)

    tk.Radiobutton(select_frame, image=pixel_image, variable=v, value=0, indicatoron=False, background=yellow_color,
                   selectcolor=yellow_color, width=20, height=20, compound='center').pack()
    tk.Radiobutton(select_frame, image=pixel_image, variable=v, value=1, indicatoron=False, background=red_color,
                   selectcolor=red_color, width=20, height=20, compound='center').pack()
    tk.Radiobutton(select_frame, image=pixel_image, variable=v, value=2, indicatoron=False, background=blue_color,
                   selectcolor=blue_color, width=20, height=20, compound='center').pack()
    tk.Radiobutton(select_frame, image=pixel_image, variable=v, value=3, indicatoron=False, background=white_color,
                   selectcolor=white_color, width=20, height=20, compound='center').pack()
    tk.Radiobutton(select_frame, image=pixel_image, variable=v, value=4, indicatoron=False, background=orange_color,
                   selectcolor=orange_color, width=20, height=20, compound='center').pack()
    tk.Radiobutton(select_frame, image=pixel_image, variable=v, value=5, indicatoron=False, background=green_color,
                   selectcolor=green_color, width=20, height=20, compound='center').pack()
    




    class Cube:
        def __init__(self):
            self.red_side = []
            self.blue_side = []
            self.yellow_side = []
            self.white_side = []
            self.green_side = []
            self.orange_side = []
            self.color_list = []
            self.select_idx = 0
            self.color_list = ['yellow', 'red', 'blue', 'white', 'orange', 'green']
            self.init_side(self.red_side, red_frame, 'red ')
            self.init_side(self.blue_side, blue_frame, 'blue ')
            self.init_side(self.yellow_side, yellow_frame, 'yellow ')
            self.init_side(self.white_side, white_frame, 'white ')
            self.init_side(self.green_side, green_frame, 'green ')
            self.init_side(self.orange_side, orange_frame, 'orange ')

        def init_side(self, side, frame, name):
            btn0 = tk.Button(frame, image=pixel_image, bg=white_color, relief=tk.GROOVE, height=40, width=40,
                             command=lambda: self.change_color(name + '0'))
            btn1 = tk.Button(frame, image=pixel_image, bg=white_color, relief=tk.GROOVE, height=40, width=40,
                             command=lambda: self.change_color(name + '1'))
            btn2 = tk.Button(frame, image=pixel_image, bg=white_color, relief=tk.GROOVE, height=40, width=40,
                             command=lambda: self.change_color(name + '2'))
            btn3 = tk.Button(frame, image=pixel_image, bg=white_color, relief=tk.GROOVE, height=40, width=40,
                             command=lambda: self.change_color(name + '3'))
            btn4 = tk.Button(frame, image=pixel_image, bg=white_color, relief=tk.GROOVE, height=40, width=40,
                             command=lambda: self.change_color(name + '4'))
            btn5 = tk.Button(frame, image=pixel_image, bg=white_color, relief=tk.GROOVE, height=40, width=40,
                             command=lambda: self.change_color(name + '5'))
            btn6 = tk.Button(frame, image=pixel_image, bg=white_color, relief=tk.GROOVE, height=40, width=40,
                             command=lambda: self.change_color(name + '6'))
            btn7 = tk.Button(frame, image=pixel_image, bg=white_color, relief=tk.GROOVE, height=40, width=40,
                             command=lambda: self.change_color(name + '7'))
            btn8 = tk.Button(frame, image=pixel_image, bg=white_color, relief=tk.GROOVE, height=40, width=40,
                             command=lambda: self.change_color(name + '8'))
            sides = [btn0, btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8]
            for i in range(9):
                sides[i].grid(row=i // 3, column=i % 3)
                side.append(sides[i])

        def change_color(self, name_str):
            name, idx = name_str.split()
            idx = int(idx)
            color = self.color_list[self.select_idx]
            if name == 'red':
                self.red_side[idx].config(background=color)
            elif name == 'blue':
                self.blue_side[idx].config(background=color)
            elif name == 'yellow':
                self.yellow_side[idx].config(background=color)
            elif name == 'green':
                self.green_side[idx].config(background=color)
            elif name == 'white':
                self.white_side[idx].config(background=color)
            elif name == 'orange':
                self.orange_side[idx].config(background=color)
    
    cube = Cube()
    cube_state.mainloop()


if __name__ == '__main__':
    cube_win()
