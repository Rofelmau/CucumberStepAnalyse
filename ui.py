from tkinter import *
from tkinter import ttk
from stepAnalyse import analyse_step_definitions
from threading import Thread
import time
from queue import Queue


class WorkThread(Thread):

    def __init__(self, root_path, file_postfix, save_result_dir, searched_data, queue):
        Thread.__init__(self)
        self.path = root_path
        self.postfix = file_postfix
        self.save_path = save_result_dir
        self.queue = queue
        self.searched_data = searched_data

    def run(self):
        steps = analyse_step_definitions(self, self.path, self.postfix, self.save_path, self.searched_data)
        self.queue.empty()
        self.queue.put(steps)


def _remove_whitespaces_at_beginning_of_string(_string):
    while _string.startswith(" "):
        _string = _string.replace(" ", "", 1)
    return _string


class Ui:

    def __init__(self):

        def callback(event):
            root_window.after(50, select_all, event.widget)

        def select_all(widget):
            widget.select_range(0, 'end')
            widget.icursor('end')

        root_window = Tk()
        root_window.title("Step Definition Scanner")
        root_window.iconbitmap('icon.ico')
        root_window.grid_columnconfigure(2, weight=1)
        root_window.grid_rowconfigure(1, weight=1)
        root_window.grid_rowconfigure(2, weight=1)
        root_window.grid_rowconfigure(3, weight=1)

        row = 0
        Label(root_window, text=" ").grid(row=row, column=0, sticky="news")

        row = 1
        Label(root_window, text="ROOT_PATH: ").grid(row=row, column=1, sticky=E)
        self.root_path = Entry(root_window, width=50)
        self.root_path.grid(row=row, column=2, columnspan=2, sticky="news")
        self.root_path.bind('<Control-a>', callback)

        row = 2
        Label(root_window, text="FILE_POSTFIX: ").grid(row=row, column=1, sticky=E)
        self.file_postfix = Entry(root_window, width=50)
        self.file_postfix.grid(row=row, column=2, columnspan=2, sticky="news")
        self.file_postfix.bind('<Control-a>', callback)

        row = 3
        Label(root_window, text="SAVE_RESULT_DIR: ").grid(row=row, column=1, sticky=E)
        self.save_result_dir = Entry(root_window, width=50)
        self.save_result_dir.grid(row=row, column=2, columnspan=2, sticky="news")
        self.save_result_dir.bind('<Control-a>', callback)

        row = 4
        Label(root_window, text=" ").grid(row=row, column=1, sticky="news")

        row = 5
        Label(root_window, text="select the data you want to collect").grid(row=row, column=1, columnspan=3,
                                                                            sticky="news")

        # needs to match order of params in class Step and class Param
        self.checkbox_values = [
            ("text", BooleanVar()),
            ("object_type", BooleanVar()),
            ("params", BooleanVar(),
             [
                 ("capture", BooleanVar()),
                 ("param_type", BooleanVar()),
                 ("param_name", BooleanVar())
             ]
             ),
            ("file_name", BooleanVar())
        ]

        col = 1
        row = 6
        for i in range(len(self.checkbox_values)):
            self.checkbox_values[i][1].set(True)
            if len(self.checkbox_values[i]) <= 2:
                checkbutton = Checkbutton(root_window, text=self.checkbox_values[i][0],
                                          variable=self.checkbox_values[i][1])
                checkbutton.grid(row=row, column=col, sticky='news')
                col += 1
                if col == 4:
                    row += 1
                    col = 1
            else:
                for j in range(0, len(self.checkbox_values[i][2])):
                    self.checkbox_values[i][2][j][1].set(True)
                    checkbutton = Checkbutton(root_window, text=self.checkbox_values[i][2][j][0],
                                              variable=self.checkbox_values[i][2][j][1])
                    checkbutton.grid(row=row, column=col, sticky='news')
                    col += 1
                    if col == 4:
                        row += 1
                        col = 1

        row = row+1  # 8
        Label(root_window, text=" ").grid(row=row, column=1, sticky="news")

        row = row+1  # 9
        self.result_label = Label(root_window, text="")
        self.result_label.grid(row=row, column=1, columnspan=3)

        row = row+1  # 10
        Label(root_window, text=" ").grid(row=row, column=6, sticky="news")

        row = row+1  # 11
        ttk.Style().configure('green/black.TButton', foreground='black', background='black')
        button_run_scan = ttk.Button(root_window, text="Run Scanner", command=self._run_scanner,
                                     style='green/black.TButton')
        button_run_scan.grid(row=row, column=1, columnspan=3, sticky="news")

        row = row+1  # 12
        Label(root_window, text=" ").grid(row=row, column=6, sticky="news")

        window_width = root_window.winfo_reqwidth()
        window_height = root_window.winfo_reqheight()
        position_horizontal = int(root_window.winfo_screenwidth() / 2 - window_width / 2)
        position_vertical = int(root_window.winfo_screenheight() / 2 - window_height / 2)
        root_window.geometry("+{}+{}".format(position_horizontal, position_vertical))
        root_window.update()
        root_window.minsize(root_window.winfo_width(), root_window.winfo_height())
        mainloop()

    def _run_scanner(self):
        search_root_path = self.root_path.get()
        search_file_postfix = self.file_postfix.get()
        save_result_dir = self.save_result_dir.get()

        search_root_path = _remove_whitespaces_at_beginning_of_string(search_root_path)
        if not search_root_path:
            self.result_label.configure(text="Please enter search path")
            return

        search_file_postfix = _remove_whitespaces_at_beginning_of_string(search_file_postfix)
        if not search_file_postfix:
            self.result_label.configure(text="Please enter file postfix")
            return

        save_result_dir = _remove_whitespaces_at_beginning_of_string(save_result_dir)
        if save_result_dir and not save_result_dir.endswith('\\') and not save_result_dir.endswith('/'):
            save_result_dir += '\\'

        self.result_label.configure(text="Running")
        self.result_label.update()
        que = Queue()
        with que.mutex:
            que.queue.clear()

        thread1 = WorkThread(search_root_path, search_file_postfix, save_result_dir, self.checkbox_values, que)
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
