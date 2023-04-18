import tkinter as tk
from tkinter import ttk
import time
from interface.section1 import Section1
from interface.section2 import Section2
from interface.section3 import Section3
from interface.section4 import Section4

class LoadingApp:
    def __init__(self, master):
        self.master = master
        master.title("Генерация голоса")
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        app_width = 800
        app_height = 400
        x = int((screen_width / 2) - (app_width / 2))
        y = int((screen_height / 2) - (app_height / 2))
        master.geometry(f"{app_width}x{app_height}+{x}+{y - 100}")
        master.resizable(False, False)
        bgm= '#696969'
        # create menu
        self.menu_frame = tk.Frame(master, width=100, height=app_height, bg=bgm)
        self.menu_frame.pack(side="left", fill="y")
        self.section1_button = tk.Button(self.menu_frame, text="🔊 ЗВУК", command=self.load_section1, width=10, pady=10, borderwidth=0, anchor='w')
        self.section1_button.pack()
        self.section2_button = tk.Button(self.menu_frame, text="🎬 МОНТАЖ", command=self.load_section2, width=10, pady=10, borderwidth=0, anchor='w')
        self.section2_button.pack()
        self.section3_button = tk.Button(self.menu_frame, text="🕸️ ПУБЛИКАЦИЯ", command=self.load_section3, width=10, pady=10, borderwidth=0, anchor='w')
        self.section3_button.pack()
        self.section4_button = tk.Button(self.menu_frame, text="💬 КОММЕНТЫ", command=self.load_section4, width=10, pady=10, borderwidth=0, anchor='w')
        self.section4_button.pack()

        # create container for sections
        self.container = tk.Frame(master, width=250, height=app_height)
        self.container.pack(side="right", fill="both", expand=True)

        self.load_section1()


    def clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def load_section1(self):
        self.clear_container()
        self.section1 = Section1(self.container)

    def load_section2(self):
        self.clear_container()
        # create section 2 if it doesn't exist yet
        if not hasattr(self, 'section2'):
            self.section2 = Section2(self.container)
        self.section2.show()

    def load_section3(self):
        self.clear_container()
        # create section 3 if it doesn't exist yet
        if not hasattr(self, 'section3'):
            self.section3 = Section3(self.container)
        self.section3.show()



    def load_section4(self):
        self.clear_container()
        # create section 4 if it doesn't exist yet
        if not hasattr(self, 'section4'):
            self.section4 = Section4(self.container)
        self.section4.show()


def main():
    root = tk.Tk()
    app = LoadingApp(root)
    root.mainloop()
