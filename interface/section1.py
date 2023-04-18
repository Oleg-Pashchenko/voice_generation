import tkinter as tk
from tkinter import ttk
import time

from main import get_status_texts, start_app
from misc.Event import event
import threading

from misc import secrets


class Section1(tk.Frame):
    def __init__(self, parent):

        super().__init__(parent)

        bgmm = '#505050'
        self.parent = parent
        self.main_name = tk.Label(self.master, text='Собрать голоса', font=('Arial', 28), )
        self.main_name.pack(side='top', pady=10)
        self.loading_label = tk.Label(self.master, text="", )
        self.loading_label.pack()

        # create status label
        self.status_label = tk.Label(self.master, text="", )
        self.status_label.pack()

        # create progressbar
        self.progressbar = ttk.Progressbar(self.master, orient="horizontal", length=200, mode="determinate")
        self.progressbar.pack(pady=10)

        # create start button
        self.start_button = tk.Button(self.master, text="Start", command=self.start_loading, )
        self.start_button.pack(pady=10)

        table_frame = tk.Frame(self.master)
        table_frame.pack()
        col0_label = tk.Label(table_frame, text="+/-", relief=tk.RAISED, width=5)
        col0_label.pack(side=tk.LEFT)
        col1_label = tk.Label(table_frame, text="Название параметра", relief=tk.RAISED, width=25)
        col1_label.pack(side=tk.LEFT)
        col2_label = tk.Label(table_frame, text="Значение", relief=tk.RAISED, width=40)
        col2_label.pack(side=tk.LEFT)
        data = secrets.secret_info
        data = [("API ключ Microsoft", data.AZURE_API_KEY),
                ("API ключ Yandex", data.YANDEX_API_KEY),
                ("API ключ Zvukogram", data.ZVUKOGRAM_API_KEY),
                ("Название таблицы", data.GOOGLE_SHEET.GOOGLE_SHEET_NAME),
                ("Код таблицы", data.GOOGLE_SHEET.GOOGLE_SPREADSHEET_ID),
                ("Путь к файлу с доступом к Google", data.GOOGLE_SHEET.GOOGLE_AUTH_FILE_NAME)]

        for data1, data2 in data:
            row_frame = tk.Frame(self.master)  # Создаем отдельный фрейм для каждой строки
            row_frame.pack()
            row_label0 = tk.Label(row_frame, text='-', relief=tk.SUNKEN, width=5)
            row_label0.pack(side=tk.LEFT)
            row_label1 = tk.Label(row_frame, text=data1, relief=tk.SUNKEN, width=25, anchor='w')
            row_label1.pack(side=tk.LEFT)
            row_label2 = tk.Label(row_frame, text=data2, relief=tk.SUNKEN, width=40, anchor='w')
            row_label2.pack(side=tk.LEFT)



    def start_loading(self):
        self.start_button.config(state="disabled")  # disable start button during loading

        # define loading strings and status texts
        loading_strings = ["Выполнение.", "Выполнение..", "Выполнение..."]
        status_texts = get_status_texts()
        thread = threading.Thread(target=start_app)
        # Запускаем поток
        thread.start()
        # loop through loading strings and status texts
        for i in range(len(status_texts)):
            while True:
                event.wait(1)
                if not event.is_set():
                    for j in range(3):
                        self.loading_label.config(text=loading_strings[j])
                        self.status_label.config(text=status_texts[i])
                        self.master.update()  # update GUI
                        time.sleep(0.25)
                else:
                    event.clear()
                    break


            self.progressbar.step(100 / len(status_texts))

        self.loading_label.config(text="")  # clear loading label
        self.status_label.config(text="Голос успешно сгенерирован!")  # set status to Done!
        self.progressbar.pack_forget()  # hide progressbar after loading
        self.start_button.pack(pady=10)  # show start button after loading

