# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 14:57:47 2019

@author: michael.mercado
"""


#You need to use the var.get(). Here's a working example in Python3.3.

from tkinter import *
import Tkinter

root=Tk()

class CheckB():
    def __init__(self, main, text):
        self.var = IntVar()
        self.text=text
        c = Checkbutton(
            main, text=text,
            variable=self.var,
            command=self.check)
        c.pack()

    def check(self):
        print (self.text, "is", self.var.get())


check1 = CheckB(root, text="Gamma")
check2 = CheckB(root, text="Beta")
check3 = CheckB(root, text="Alpha")


text = "Great"
root = Tkinter.Tk()
root.mainloop()

CheckB(root,text)

