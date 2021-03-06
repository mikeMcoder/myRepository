# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 16:54:42 2019

@author: michael.mercado
"""
import Tkinter as Tk

#create class MainGui
#esablish the size of the rootwindow

class CheckButton():
    def __init__(self, master, text):
        self.var = Tk.IntVar()
        self.text=text
        c = Tk.Checkbutton(
            master, text=text,
            variable=self.var,
            command=self.check)
        #c.pack()
    
    def check(self):
        try:
            self.var1 = self.var.get()
            print (self.text, "is", self.var1)
            return self.var1
        except:
            raise

class StartButton():
    def __init__(self):
        pass

class MainGui:
    def __init__(self):
        
        self.root = Tk.Tk()         #get the root window
        self.root.title("RT GUI")   # add a title to the root window
        self.root.geometry("800x800")# this is the size of the main window
        #layout containers
        self.root.grid_rowconfigure(1, weight = 1)
        self.root.grid_columnconfigure(0, weight = 
        
        #create the containers or frames color blue
        self.frame = Tk.Frame(master = self.root,bg = 'blue', width=100, height=100,\
                              pady = 1)
       
        #assign a location for this frame
        self.frame.grid(row = 0, sticky = 'ws')
        
        #add the check buttons
        self.addCheckbutton()
        
        
        
1)
   
    def addCheckbutton(self):
        self.check1 = CheckButton(self.frame, text="RandomFrequencyTest")
        self.check2 = CheckButton(self.frame, text="RandomPowerTest")
        self.check3 = CheckButton(self.frame, text="RandomFtfTest")
        
    def sampleProgram(self):
        print ("Running a program...")
        
    def RunEngine(self):
        
        
        try:
            self.check1(command = self.sampleProgram)
            
        except:
            pass
            
        
        
#initialize parameters
#create root window
#create selection buttons
#attach start button
#attach stop button


if __name__=='__main__':
    gui = MainGui()
    gui.root.mainloop()
    
    