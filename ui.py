from tkinter import *
from tkinter import ttk
from stepAnalyse import analyse_step_definitions


class Ui:

    def __init__(self):
        root_indow = Tk()
        root_indow.title("Step Analyse")

        Label(root_indow, text="ROOT_PATH: ").grid(row=1, column=1, sticky=W)

        self.root_path = Entry(root_indow)
        self.root_path.grid(row=1, column=2, columnspan=2)

        Label(root_indow, text="FILE_POSTFIX: ").grid(row=2, column=1, sticky=W)

        self.file_postfix = Entry(root_indow)
        self.file_postfix.grid(row=2, column=2, columnspan=2)

        Label(root_indow, text=" ").grid(row=0, column=0, sticky=W)
        Label(root_indow, text=" ").grid(row=3, column=1, sticky=W)
        Label(root_indow, text=" ").grid(row=5, column=4, sticky=W)

        ttk.Style().configure('green/black.TButton', foreground='black', background='black')
        b = ttk.Button(root_indow, text="Run Scanner", command=self._run_scanner, style='green/black.TButton')
        b.grid(row=4, column=1, columnspan=3)

        window_width = root_indow.winfo_reqwidth()
        window_height = root_indow.winfo_reqheight()
        position_horizontal = int(root_indow.winfo_screenwidth() / 2 - window_width / 2)
        position_vertical = int(root_indow.winfo_screenheight() / 2 - window_height / 2)
        root_indow.geometry("+{}+{}".format(position_horizontal, position_vertical))

        mainloop()

    def _run_scanner(self):
        analyse_step_definitions(self, self.root_path.get(), self.file_postfix.get())
        print(self.root_path.get())
