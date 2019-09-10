from tkinter import *
from tkinter import ttk
from stepAnalyse import analyse_step_definitions
from threading import Thread
import time
from queue import Queue


class WorkThread (Thread):

    def __init__(self, root_path, file_postfix, queue):
        Thread.__init__(self)
        self.path = root_path
        self.postfix = file_postfix
        self.queue = queue

    def run(self):
        steps = analyse_step_definitions(self, self.path, self.postfix)
        self.queue.empty()
        self.queue.put(steps)


class Ui:

    def __init__(self):
        root_window = Tk()
        root_window.title("Step Definition Scanner")
        root_window.iconbitmap('icon.ico')
        root_window.grid_columnconfigure(2, weight=1)
        root_window.grid_rowconfigure(1, weight=1)
        root_window.grid_rowconfigure(2, weight=1)
        root_window.grid_rowconfigure(3, weight=1)

        Label(root_window, text="ROOT_PATH: ").grid(row=1, column=1, sticky=E)
        self.root_path = Entry(root_window)
        self.root_path.grid(row=1, column=2, columnspan=2, sticky="news")

        Label(root_window, text="FILE_POSTFIX: ").grid(row=2, column=1, sticky=E)
        self.file_postfix = Entry(root_window)
        self.file_postfix.grid(row=2, column=2, columnspan=2, sticky="news")

        Label(root_window, text=" ").grid(row=0, column=0, sticky="news")
        Label(root_window, text=" ").grid(row=3, column=1, sticky="news")
        self.result_string = StringVar()
        self.result_string.set("")
        # Label(root_window, textvariable=self.result_string).grid(row=4, column=1, columnspan=3)
        self.result_label = Label(root_window, text="")
        self.result_label.grid(row=4, column=1, columnspan=3)
        Label(root_window, text=" ").grid(row=5, column=1, sticky="news")
        Label(root_window, text=" ").grid(row=7, column=6, sticky="news")

        ttk.Style().configure('green/black.TButton', foreground='black', background='black')
        button_run_scan = ttk.Button(root_window, text="Run Scanner", command=self._run_scanner, style='green/black.TButton')
        button_run_scan.grid(row=6, column=1, columnspan=3, sticky="news")

        window_width = root_window.winfo_reqwidth()
        window_height = root_window.winfo_reqheight()
        position_horizontal = int(root_window.winfo_screenwidth() / 2 - window_width / 2)
        position_vertical = int(root_window.winfo_screenheight() / 2 - window_height / 2)
        root_window.geometry("+{}+{}".format(position_horizontal, position_vertical))

        mainloop()

    def _run_scanner(self):
        self.result_label.configure(text="Running")
        self.result_label.update()
        que = Queue()
        with que.mutex:
            que.queue.clear()

        thread1 = WorkThread(self.root_path.get(), self.file_postfix.get(), que)
        thread1.start()

        x = 0
        while thread1.isAlive():
            time.sleep(1)
            x += 1
            dots = ' '
            v = 0
            while v < x:
                dots += '. '
                v += 1
            if x == 5:
                x = 0
            self.result_label.configure(text="Running \n" + dots)
            self.result_label.update()

        text_steps_found = str(que.get())
        self.result_label.configure(text="Done \n" + text_steps_found + " Step Deifionitions Found")
        self.result_label.update()
