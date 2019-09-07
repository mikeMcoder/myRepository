# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 10:56:43 2019

@author: michael.mercado
"""

import tkinter as tk
from tkinter import ttk


class GuiButtons:
    def __init__(self):
        self.ttk = ttk
        self.tk = tk
        self.root = self.tk.Tk()
        self.makeButton1()
        self.makeButton2()
        self.root.mainloop()
        
    def callback1(self):
        print "Let's print callback1"
        
    def callback2(self):
        print "Let's print callback2"

    def makeButton1(self):
        button = self.ttk.Button(text = "BUTTON1",command = self.callback1)
        self.ttk.Style().configure("TButton", padding=6, relief="flat",
   background="black", foreground = "blue")
        button.pack()
          
    def makeButton2(self):
        self.ttk.Style().configure("TButton", padding=6, relief="flat",
   background="black", foreground = "white")
        button = self.ttk.Button(text = "BUTTON2",command = self.callback2)
        button.pack()
        
        
        
b = GuiButtons()


