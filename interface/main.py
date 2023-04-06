import tkinter as tk
from tkinter import ttk
import time

class LoadingApp:
    def __init__(self, master):
        self.master = master
        master.title("Генерация голоса")
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        app_width = 350
        app_height = 200
        x = int((screen_width / 2) - (app_width / 2))
        y = int((screen_height / 2) - (app_height / 2))
        master.geometry(f"{app_width}x{app_height}+{x}+{y - 100}")
        self.main_name = tk.Label(master, text='Генерация голоса', font=('Arial', 28))
        self.main_name.pack(side='top', pady=10)
        master.resizable(False, False)
        self.loading_label = tk.Label(master, text="")
        self.loading_label.pack()

        # create status label
        self.status_label = tk.Label(master, text="")
        self.status_label.pack()

        # create progressbar
        self.progressbar = ttk.Progressbar(master, orient="horizontal", length=200, mode="determinate")
        self.progressbar.pack(pady=10)

        # create start button
        self.start_button = tk.Button(master, text="Start", command=self.start_loading)
        self.start_button.pack(pady=10)

    def start_loading(self):
        self.start_button.config(state="disabled") # disable start button during loading

        # define loading strings and status texts
        loading_strings = ["Выполнение.", "Выполнение..", "Выполнение..."]
        status_texts = ["Создание файла Russian", "Создание файла English",
                        "Создание файла Dutch", "Создание файла France",
                        'Финальная обработка...']

        # loop through loading strings and status texts
        for i in range(4):
            for j in range(3):
                self.loading_label.config(text=loading_strings[j])
                self.status_label.config(text=status_texts[i])
                self.master.update() # update GUI
                time.sleep(0.5) # simulate loading time
            self.progressbar.step(25)

        self.loading_label.config(text="") # clear loading label
        self.status_label.config(text="Голос успешно сгенерирован!") # set status to Done!
        self.progressbar.pack_forget() # hide progressbar after loading
        self.start_button.pack(pady=10) # show start button after loading
        #self.start_button.config(state="normal") # re-enable start button

root = tk.Tk()
app = LoadingApp(root)
root.mainloop()
