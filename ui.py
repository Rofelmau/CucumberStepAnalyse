from tkinter import *
from tkinter import ttk
from stepAnalyse import analyse_step_definitions


class Ui:

    def __init__(self):
        root_window = Tk()
        root_window.title("Step Analyse")

        Label(root_window, text="ROOT_PATH: ").grid(row=1, column=1, sticky=W)

        self.root_path = Entry(root_window)
        self.root_path.grid(row=1, column=2, columnspan=2)

        Label(root_window, text="FILE_POSTFIX: ").grid(row=2, column=1, sticky=W)

        self.file_postfix = Entry(root_window)
        self.file_postfix.grid(row=2, column=2, columnspan=2)

        Label(root_window, text=" ").grid(row=0, column=0, sticky=W)
        Label(root_window, text=" ").grid(row=3, column=1, sticky=W)
        self.result_string = StringVar()
        self.result_string.set("")
        Label(root_window, textvariable=self.result_string).grid(row=4, column=1, columnspan=3)
        Label(root_window, text=" ").grid(row=5, column=1, sticky=W)
        Label(root_window, text=" ").grid(row=7, column=6, sticky=W)

        ttk.Style().configure('green/black.TButton', foreground='black', background='black')
        b = ttk.Button(root_window, text="Run Scanner", command=self._run_scanner, style='green/black.TButton')
        b.grid(row=6, column=1, columnspan=3)

        window_width = root_window.winfo_reqwidth()
        window_height = root_window.winfo_reqheight()
        position_horizontal = int(root_window.winfo_screenwidth() / 2 - window_width / 2)
        position_vertical = int(root_window.winfo_screenheight() / 2 - window_height / 2)
        root_window.geometry("+{}+{}".format(position_horizontal, position_vertical))

        mainloop()

    def _run_scanner(self):
        self.result_string.set("")
        found_steps = analyse_step_definitions(self, self.root_path.get(), self.file_postfix.get())
        self.result_string.set("Done \n" + str(found_steps) + " Step Deifionitions Found")
