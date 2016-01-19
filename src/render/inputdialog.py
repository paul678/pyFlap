from tkinter import *


class InputDialog:
    def __init__(self, parent):
        top = self.top = Toplevel(parent)

        Label(top, text="Value").pack()

        self.e = Entry(top)
        self.e.pack(padx=5)

        b = Button(top, text="OK", command=self.ok)
        b.pack(pady=5)

    def ok(self):
        self.value = self.e.get();
        self.top.destroy()
